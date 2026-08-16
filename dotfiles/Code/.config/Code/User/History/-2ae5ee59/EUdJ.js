import GObject from "gi://GObject";
import St from "gi://St";
import Clutter from "gi://Clutter";
import GLib from "gi://GLib";

import {
  Extension,
  gettext as _,
} from "resource:///org/gnome/shell/extensions/extension.js";
import * as PanelMenu from "resource:///org/gnome/shell/ui/panelMenu.js";
import * as Main from "resource:///org/gnome/shell/ui/main.js";

const Indicator = GObject.registerClass(
  class Indicator extends PanelMenu.Button {
    _init(settings) {
      super._init(0.0, _("No Time For Caution"));
      this.settings = settings;

      this.label = new St.Label({
        text: _("Calculating..."),
        y_align: Clutter.ActorAlign.CENTER,
      });
      this.add_child(this.label);

      this._updateCountdown();
      this._timeout = GLib.timeout_add_seconds(GLib.PRIORITY_DEFAULT, 1, () => {
        this._updateCountdown();
        return GLib.SOURCE_CONTINUE;
      });
    }

    _updateCountdown() {
      let goalUnix = this.settings.get_int64("goal-time");

      // Convert goal time to local time
      let goalLocal = GLib.DateTime.new_from_unix_utc(goalUnix).to_local();
      let now = GLib.DateTime.new_now_local();

      // Calculate time difference in seconds
      let diff = goalLocal.to_unix() - now.to_unix();

      if (diff <= 0) {
        this.label.set_text(_("Goal Reached"));
      } else {
        let unit = this.settings.get_string("time-unit");
        let timeString;

        switch (unit) {
          case "hours_minutes":
            const totalMinutes = Math.floor(diff / 60);
            const hours = Math.floor(totalMinutes / 60);
            const minutes = totalMinutes % 60;
            timeString = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')} ${_("left")}`;
            break;
          case "years":
            timeString = `${(diff / 31536000).toFixed(2)} ${_("Years Remaining")}`;
            break;
          case "months":
            timeString = `${(diff / 2592000).toFixed(2)} ${_("Months Remaining")}`;
            break;
          case "weeks":
            timeString = `${(diff / 604800).toFixed(2)} ${_("Weeks Remaining")}`;
            break;
          case "days":
            timeString = `${(diff / 86400).toFixed(2)} ${_("Days Remaining")}`;
            break;
          case "hours":
            timeString = `${(diff / 3600).toFixed(2)} ${_("Hours Remaining")}`;
            break;
          case "minutes":
            timeString = `${(diff / 60).toFixed(2)} ${_("min left")}`;
            break;
          case "seconds":
            timeString = `${diff} ${_("sec left")}`;
            break;
          default:
            timeString = `${diff} ${_("Seconds Remaining")}`;
        }
        this.label.set_text(timeString);
      }
    }

    destroy() {
      if (this._timeout) {
        GLib.source_remove(this._timeout);
        this._timeout = null;
      }
      super.destroy();
    }
  }
);

export default class NoTimeForCautionExtension extends Extension {
  enable() {
    this.settings = this.getSettings();
    this._indicator = new Indicator(this.settings);
    Main.panel.addToStatusArea(
      "no-time-for-caution@ans-ibrahim.github",
      this._indicator,
      this.settings.get_int("indicator-index"),
      this.settings.get_string("indicator-position")
    );
    this.settings.connect("changed::goal-time", this._onGoalTimeChanged.bind(this));
    this.settings.connect("changed::time-unit", this._onTimeUnitChanged.bind(this));
    this.settings.connect("changed::indicator-index", this._onIndicatorPositionChanged.bind(this));
    this.settings.connect("changed::indicator-position", this._onIndicatorPositionChanged.bind(this));
  }

  _onGoalTimeChanged() {
    if (this._indicator) {
      this._indicator._updateCountdown();
    }
  }

  _onTimeUnitChanged() {
    if (this._indicator) {
      this._indicator._updateCountdown();
    }
  }

  _onIndicatorPositionChanged() {
    if (this._indicator) {
      Main.panel.removeFromStatusArea(this._indicator);
      Main.panel.addToStatusArea(
        "no-time-for-caution@ans-ibrahim.github",
        this._indicator,
        this.settings.get_int("indicator-index"),
        this.settings.get_string("indicator-position")
      );
    }
  }

  disable() {
    if (this._indicator) {
      this._indicator.destroy();
      this._indicator = null;
    }
    this.settings.disconnect("changed::goal-time", this._onGoalTimeChanged.bind(this));
    this.settings.disconnect("changed::time-unit", this._onTimeUnitChanged.bind(this));
    this.settings.disconnect("changed::indicator-index", this._onIndicatorPositionChanged.bind(this));
    this.settings.disconnect("changed::indicator-position", this._onIndicatorPositionChanged.bind(this));
    this.settings = null;
  }
}