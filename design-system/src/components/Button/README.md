# Button

Pill buttons: one clay primary per view, ink-outlined secondary, quiet on sunk, and round icon buttons.

- **Primary**: `action` fill, `ink` text at 600, `radius-pill`. The one main action of the view. Never white text.
- **Secondary**: `sheet` fill, 1px `ink` border. Other actions.
- **Quiet**: `sunk` fill, no border. Cancel, toolbar actions.
- **Icon**: a `target`-sized disc on `sunk`, 1.5px stroke icon, `aria-label` required.
- **Disabled**: `stone` text on `sunk`, no border.

Height at least `target` (32px) in the desktop app, 44px on touch and the web. Labels are a verb plus an object: "Place slab", not "OK".
