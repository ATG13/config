import { StateGraph, START } from "@langchain/langgraph";
import { HumanMessage, AIMessage } from "@langchain/core/messages";
import { GraphState } from "./state";
import { SYSTEM_PROMPT } from "./system-prompt";
import type { Env } from "./index";

interface NodeConfig {
  configurable?: {
    env?: Env;
  };
}

async function loadHistory(state: typeof GraphState.State, config?: NodeConfig) {
  const env = config?.configurable?.env;
  if (!env?.DB) return {};

  const rows = await env.DB.prepare(
    `SELECT role, content FROM conversations
     WHERE phone = ? AND created_at > datetime('now', '-24 hours')
     ORDER BY created_at ASC`
  ).bind(state.phone).all() as { results?: { role: string; content: string }[] };

  if (!rows.results?.length) return {};

  const historyMessages = rows.results.map((row) =>
    row.role === "user"
      ? new HumanMessage(row.content)
      : new AIMessage(row.content)
  );

  return { messages: [...historyMessages, ...state.messages] };
}

async function generateResponse(state: typeof GraphState.State, config?: NodeConfig) {
  const env = config?.configurable?.env;
  if (!env?.GOOGLE_API_KEY) {
    return { response: "I'm sorry, the AI service is not configured. Please try again later." };
  }

  // const modelName = env.GOOGLE_MODEL ?? "gemma-4-26b-a4b-it";
  const modelName = env.GOOGLE_MODEL ?? "gemini-2.0-flash";

  // Build contents: system prompt as first turn (works with all models)
  const contents: { role: string; parts: { text: string }[] }[] = [
    { role: "user", parts: [{ text: SYSTEM_PROMPT }] },
    { role: "model", parts: [{ text: "I understand. I am EMI Genie. How can I help you with your home loan queries?" }] },
  ];

  for (const msg of state.messages) {
    contents.push({
      role: msg.getType() === "human" ? "user" : "model",
      parts: [{ text: msg.content as string }],
    });
  }

  try {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${env.GOOGLE_API_KEY}`;
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ contents }),
    });

    const data = await response.json() as any;

    if (!response.ok) {
      console.error("Gemma API error:", response.status, JSON.stringify(data));
      return { response: "I'm sorry, I encountered an error processing your request. Please try again or schedule a callback for assistance." };
    }

    const parts = data?.candidates?.[0]?.content?.parts ?? [];
    const text = parts.filter((p: any) => p.text).pop()?.text;
    if (!text) {
      console.error("Gemma API: empty response", JSON.stringify(data));
      return { response: "I'm sorry, I couldn't generate a response. Please try again." };
    }

    return { response: text };
  } catch (error) {
    console.error("Gemma API fetch error:", error);
    return { response: "I'm sorry, I encountered an error processing your request. Please try again or schedule a callback for assistance." };
  }
}

async function saveAndSend(state: typeof GraphState.State, config?: NodeConfig) {
  const env = config?.configurable?.env;
  if (!env) return {};

  if (env.DB) {
    const stmt = env.DB.prepare(
      "INSERT INTO conversations (phone, role, content) VALUES (?, 'assistant', ?)"
    );
    await stmt.bind(state.phone, state.response).run();
  }

  const url = `https://graph.facebook.com/v18.0/${env.WHATSAPP_PHONE_NUMBER_ID}/messages`;
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${env.WHATSAPP_TOKEN}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      messaging_product: "whatsapp",
      to: state.phone,
      type: "text",
      text: { body: state.response },
    }),
  });

  if (!response.ok) {
    const error = await response.text();
    console.error("WhatsApp send error:", error);
  }

  return {};
}

export function buildGraph() {
  return new StateGraph(GraphState)
    .addNode("loadHistory", loadHistory)
    .addNode("generateResponse", generateResponse)
    .addNode("saveAndSend", saveAndSend)
    .addEdge(START, "loadHistory")
    .addEdge("loadHistory", "generateResponse")
    .addEdge("generateResponse", "saveAndSend")
    .addEdge("saveAndSend", "__end__")
    .compile();
}
