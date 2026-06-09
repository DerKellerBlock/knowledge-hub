# Godot Gotchas — Was nicht funktioniert hat

> Einträge hier werden vom Agent automatisch angelegt: "Füge das zu den Gotchas hinzu."
>
> Template: Problem → Ursache → Workaround → Datum → Status

## Jolt Physics + CharacterBody3D
- **Problem:** CharacterBody3D fällt durch den Boden bei Jolt Physics in Godot 4.6
- **Ursache:** `move_and_slide()` ruft `PhysicsServer3D.body_test_motion()` auf, Jolt interpretiert `safe_margin` anders
- **Workaround:** `safe_margin = 0.001` setzen oder GodotPhysics nutzen
- **Datum:** 2026-06-03
- **Status:** Workaround funktioniert

## GLB-Import Scale mit Meshy
- **Problem:** GLB-Modell unsichtbar weil scale zu klein
- **Ursache:** Meshy liefert Modelle mit unterschiedlichen nativen Größen
- **Workaround:** `auto_size: true` + `origin_at: bottom` im API-Call, dann `ChurchData.scale` kalibrieren
- **Datum:** 2026-06-08
- **Status:** Erledigt, dokumentiert in docs/ai/known-issues.md
