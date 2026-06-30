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

## Area3D Gravity Override + CharacterBody3D
- **Problem:** `CharacterBody3D.get_gravity()` ignoriert Area3D-Gravity-Overrides (RigidBody3D respektiert sie)
- **Ursache:** Bug in `get_gravity()` — Area3D `gravity_point` / `gravity_direction` / `gravity_space_override` werden nicht ausgewertet
- **Workaround:** Eigene Gravity-Berechnung: Area3D-Nodes im `gravity_space_override`-Mode manuell abfragen und Gravity-Vektor selbst berechnen
- **Datum:** 2025-11-12 (GitHub Issue #112656, confirmed, open)
- **Status:** Bug offen, Workaround verfügbar

## Jolt: move_and_collide() aus _process() liefert null collision
- **Problem:** `move_and_collide()` aus `_process()` (nicht `_physics_process()`) mit Jolt Physics liefert manchmal null collision
- **Ursache:** Jolt Physics erwartet Physics-Ticks in `_physics_process()`; `_process()` läuft mit variablem Delta
- **Workaround:** `move_and_collide()` immer in `_physics_process()` aufrufen. Fixed in Godot 4.7.
- **Datum:** 2026-03-26 (GitHub Issue #117857, fixed in 4.7)
- **Status:** Fixed in 4.7, Workaround für 4.6

## Jolt: apply_floor_snap() katapultiert auf AnimatableBody3D
- **Problem:** `apply_floor_snap()` auf AnimatableBody3D katapultiert CharacterBody3D wenn `velocity.y` kleiner positiver Wert
- **Ursache:** `apply_floor_snap()` interagiert falsch mit AnimatableBody3D-Kollision bei Jolt
- **Workaround:** Vor `apply_floor_snap()` prüfen: `if is_zero_approx(velocity.y): velocity.y = 0`
- **Datum:** 2025-11-02 (GitHub Issue #112315, open)
- **Status:** Bug offen, Workaround verfügbar

## Jolt: Reparenting CharacterBody3D triggert ferne Area3D
- **Problem:** Reparenting CharacterBody3D mit `KeepGlobalTransform=true` triggert ferne Area3D-Nodes am World Origin
- **Ursache:** Jolt Physics wertet Area3D-Overlaps bei Reparenting falsch aus (nicht Godot Physics)
- **Workaround:** Area3D-Nodes temporär deaktivieren vor Reparenting, oder GodotPhysics nutzen
- **Datum:** 2025-11-22 (GitHub Issue #113058, confirmed, open)
- **Status:** Bug offen, Workaround verfügbar

## GLB-Import Scale mit Meshy
- **Problem:** GLB-Modell unsichtbar weil scale zu klein
- **Ursache:** Meshy liefert Modelle mit unterschiedlichen nativen Größen
- **Workaround:** `auto_size: true` + `origin_at: bottom` im API-Call, dann `ChurchData.scale` kalibrieren
- **Datum:** 2026-06-08
- **Status:** Erledigt, dokumentiert in docs/ai/known-issues.md

## GLB-Import — Mesh Origin Bug
- **Problem:** Mesh origin point verschiebt sich vom World Origin weg beim Skalieren importierter GLB/OBJ-Geometrie (nicht bei Godot-nativen QuadMesh)
- **Ursache:** Bug in Godots GLB/OBJ-Importer — "Generate LODs" ist Teil der Reproduktion
- **Workaround:** "Generate LODs" im Import-Dialog deaktivieren als Diagnose-Schritt. Kein vollständiger Fix bekannt.
- **Datum:** 2025-10-14 (GitHub Issue #111653, open)
- **Status:** Bug offen, kein vollständiger Fix
