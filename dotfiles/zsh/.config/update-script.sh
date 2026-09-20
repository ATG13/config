#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "==> Updating system packages via DNF..."
sudo dnf upgrade -y

echo "==> Upgrading OpenCode..."
opencode upgrade

echo "==> Updating Oh My Pi (omp)..."
omp update

echo "==> Updating Herdr..."
herdr update

echo "==> All updates completed successfully!"
