# Godot RST Parser Rewrite — Implementation Plan

> **Status:** Plan — ready for implementation
> **Created:** 2026-06-10
> **Spec:** Real RST format analyzed from `godot-docs-reference-packed.md` (457,636 lines, 1,078 class files, 33 tutorial files)

## Problem

The current `domains/godot/parser.py` produces **0 structured chunks** from real Godot RST. It tries to match `.. class:: ClassName` (Sphinx directive notation), but the actual packed file uses the official Godot RST format: class anchors (`.. _class_Node3D:`), RST tables for properties/methods, and per-member description blocks. The real format is very different from what the parser expects.

Every chunk currently falls through to `fallback_chunk()` — brute-force 500-token sliding windows. This means search results have no structured metadata (`chunk_type`, `class_name`, `name`, `signature`), no inheritance chains for boosting, and no clean text for embedding.

## Target State

After rewrite, the parser must extract **structured Chunk objects** from 1,078 class files in the packed source, yielding roughly:
- ~1,078 class overview chunks
- ~20,000+ method chunks
- ~10,000+ property chunks
- ~1,500+ signal chunks
- ~500+ enum chunks  
- ~3,000+ constant chunks

Non-class content (33 tutorial files under `getting_started/`) falls through to `fallback_chunk()` as before — no change needed.

---

## 1. Files Affected

| File | Action | Risk |
|------|--------|------|
| `domains/godot/parser.py` | **Rewrite** (complete replacement) | Low — self-contained, no other files import it directly |
| `domains/godot/domain.md` | **No change needed** | — metadata already references `rst-godot` parser |
| `scripts/parser_base.py` | **Update chunk_type comment** | Add `"operator"`, `"constructor"`, `"annotation"`, `"theme_property"` to the `chunk_type` field comment (line 33). The dataclass needs no code change — `chunk_type: str | None` already accepts any string. Only the documentation comment must list the new values. |
| `scripts/embed_index.py` | **No change needed** | Already calls `parser.parse()` and falls back correctly |
| `docs/ai/known-issues.md` | **Update** | Remove LIM-002 (0 structured chunks limitation) |

---

## 2. Real RST Format — Complete Reference

### 2.1 File Boundaries (packed file)

Each class starts with a repomix file header:
```
## File: classes/class_node3d.rst
`````````rst
...RST content...
`````````
```

The next `## File:` header marks the boundary. Tutorial files use `## File: getting_started/...`.

**Pattern:**
```python
FILE_BOUNDARY = re.compile(r'^## File: (classes/class_(\w+)\.rst|getting_started/.+)')
```

### 2.2 Class Header

```
.. _class_Node3D:

Node3D
======

**Inherits:** :ref:`Node<class_Node>` **<** :ref:`Object<class_Object>`

**Inherited By:** :ref:`AudioListener3D<class_AudioListener3D>`, ...

Description
-----------

The **Node3D** node is the base representation of a node in 3D space...
```

**Extract:**
- Class name from `.. _class_([\w@]+):` anchor (not the `======` header) — handles `@GDScript`, `@GlobalScope`
- Inheritance from `**Inherits:**` line by extracting text from `:ref:`name<link>`
- Description from text between Description header and next `.. rst-class::` directive

### 2.3 Properties Table & Property Descriptions

**Table section (summary):**
```
.. rst-class:: classref-reftable-group

Properties
----------

.. table::
   :widths: auto

   +-------------------------------------------------------+-------------------------------------------------------------------------------+
   | :ref:`Vector3<class_Vector3>`                         | :ref:`global_position<class_Node3D_property_global_position>`                 |
   +-------------------------------------------------------+-------------------------------------------------------------------------------+
```

Each property name is in the **second column** of the table: `:ref:`name<class_XXX_property_name>``.

**Property descriptions (later in document):**
```
.. _class_Node3D_property_basis:

.. rst-class:: classref-property

:ref:`Basis<class_Basis>` **basis** :ref:`🔗<class_Node3D_property_basis>`

.. rst-class:: classref-property-setget

- |void| **set_basis**\ (\ value\: :ref:`Basis<class_Basis>`\ )
- :ref:`Basis<class_Basis>` **get_basis**\ (\ )

Basis of the transform property...
```

Property description anchored by `.. _class_XXX_property_NAME:`.

**Theme properties** use a distinct anchor pattern and appear in classes like AcceptDialog and Button. There are 6 theme sub-types: `theme_constant` (~540), `theme_color` (~626), `theme_icon` (~552), `theme_style` (~439), `theme_font` (~267), and `theme_font_size` (~27). All map to `chunk_type='theme_property'`.

Example anchors: `.. _class_AcceptDialog_theme_constant_buttons_min_height:`, `.. _class_Button_theme_color_font_color:`, `.. _class_Button_theme_style_normal:`.

### 2.4 Methods Table & Method Descriptions

**Table section:**
```
Methods
-------

.. table::
   :widths: auto

   +--------------------------------------------------------------------+
   | |void|  :ref:`rotate_y<class_Node3D_method_rotate_y>`\ (\ angle\: ... |
   +--------------------------------------------------------------------+
```

Methods are in the **rightmost column** of the table. Format: `|type|| :ref:`name<class_XXX_method_name>`\ (\ params\ )`. Return types like `|void|`, `:ref:`Vector3<class_Vector3>|`, etc.

**Method descriptions (regular methods):**
```
.. _class_Node3D_method_rotate_y:

.. rst-class:: classref-method

|void| **rotate_y**\ (\ angle\: :ref:`float<class_float>`\ ) :ref:`🔗<class_Node3D_method_rotate_y>`

Rotates this node's basis around the Y axis by the given ``angle``...
```

**Special method variants** use different RST member types in the anchor:

| Anchor Pattern | RST Type | chunk_type | Example |
|---------------|---------|-----------|---------|
| `.. _class_X_method_NAME:` | Regular method | `method` | `_class_Node3D_method_rotate_y:` |
| `.. _class_X_operator_NAME:` | Operator overload | `operator` | `_class_AABB_operator_neq_AABB:` |
| `.. _class_X_constructor_NAME:` | Constructor | `constructor` | `_class_AABB_constructor_AABB:` |
| `.. _class_X_private_method_NAME:` | Virtual method | `method` | `_class_AnimationMixer_private_method__post_process_key_value:` |

All variants share the same description block structure (anchor → `classref-method` → signature → description). The parser extracts the member type from the anchor group and maps it to the appropriate `chunk_type`.

Separated by `.. rst-class:: classref-item-separator` / `----`.

### 2.5 Signals

**Signal descriptions:**
```
.. _class_Node3D_signal_visibility_changed:

.. rst-class:: classref-signal

**visibility_changed**\ (\ ) :ref:`🔗<class_Node3D_signal_visibility_changed>`

Emitted when this node's visibility changes...
```

Some classes may have a Signals table (same table structure as Methods). Others (like Node3D) only have descriptions. The parser must handle both cases.

### 2.6 Enums

```
.. _enum_Node3D_RotationEditMode:

.. rst-class:: classref-enumeration

enum **RotationEditMode**: :ref:`🔗<enum_Node3D_RotationEditMode>`

.. _class_Node3D_constant_ROTATION_EDIT_MODE_EULER:

.. rst-class:: classref-enumeration-constant

:ref:`RotationEditMode<enum_Node3D_RotationEditMode>` **ROTATION_EDIT_MODE_EULER** = ``0``

The rotation is edited using Euler angles...
```

Also in descriptions, inline in class text: `enum **Name**:` without anchor.

**Special enum names** may contain `@` (e.g., `.. _enum_@GlobalScope_Variant.Type:`) and `.` (e.g., `Variant.Type`). The enum anchor regex uses `[\w@.]+` to capture these characters correctly.

### 2.7 Constants

```
.. _class_Node3D_constant_NOTIFICATION_TRANSFORM_CHANGED:

.. rst-class:: classref-constant

**NOTIFICATION_TRANSFORM_CHANGED** = ``2000`` :ref:`🔗<...>`

Notification received when...
```

Also in `@GDScript`:
```
.. _class_@GDScript_constant_PI:

.. rst-class:: classref-constant

**PI** = ``3.14159265358979`` :ref:`🔗<class_@GDScript_constant_PI>`

Description text...
```

### 2.8 Section Separators

```
.. rst-class:: classref-section-separator

----

.. rst-class:: classref-descriptions-group

Signals
-------
```

The `classref-descriptions-group` markers indicate the start of: Signals, Enumerations, Constants, Property Descriptions, Method Descriptions sections.

---

## 3. Parser State Machine (Single-Pass)

The new parser uses a **single-pass approach** with a state machine that processes each class block immediately upon detection: file boundary detection and structured parsing happen in the same loop.

### 3.1 File Splitting & Class Detection (Within Single Pass)

```
Input: entire packed file content (457K lines, one big string)
Output: list of (class_name, start_line, end_line, is_class_file) tuples

Algorithm:
  Scan line-by-line
  When "## File: classes/class_X.rst" → note file boundary
  Within the file, look for ".. _class_X:" anchor
  If found → is_class_file = True, extract class_name
  Continue until next "## File:" boundary
  
  For non-class files (getting_started/) → mark is_class_file = False
```

### 3.2 Per-Class Structured Parsing (Within Single Pass)

For each class block identified in Pass 1, run Pass 2:

```
State Machine States:
  INIT                   → scanning for class anchor
  CLASS_HEADER           → reading class overview, inherits
  PROPERTIES_TABLE       → inside Properties table (extracting names)
  METHODS_TABLE          → inside Methods table (extracting names+signatures)
  SIGNALS_TABLE          → inside Signals table (if present)
  DESCRIPTIONS           → inside classref-descriptions-group section
  PROPERTY_DESC          → processing property description blocks
  METHOD_DESC            → processing method description blocks
  SIGNAL_DESC            → processing signal description blocks
  ENUM_DESC              → processing enum description blocks
  CONSTANT_DESC          → processing constant description blocks
  DONE                   → reached next file boundary
```

**Transitions:**

```
INIT:
  ".. _class_X:" → CLASS_HEADER
  
CLASS_HEADER:
  "Properties" header → PROPERTIES_TABLE
  (collect description text until then)

PROPERTIES_TABLE:
  Each table row → extract property name from 2nd column
  Empty line after table end → INIT (or next table)
  "Methods" header → METHODS_TABLE
  
METHODS_TABLE:
  Each table row → extract method name from rightmost column
  Empty line after table end → INIT
  "Signals" header → SIGNALS_TABLE

SIGNALS_TABLE: (optional, some classes)
  Each table row → extract signal name
  Empty line after table end → INIT

DESCRIPTIONS: (triggered by "classref-descriptions-group")
  "Signals" sub-header → SIGNAL_DESC
  "Enumerations" sub-header → ENUM_DESC
  "Constants" sub-header → CONSTANT_DESC
  "Property Descriptions" → PROPERTY_DESC
  "Method Descriptions" → METHOD_DESC

PROPERTY_DESC:
  ".. _class_X_property_NAME:" → extract property description chunk
  "classref-item-separator" or next ".. _" → ready for next

METHOD_DESC:
  ".. _class_X_method_NAME:" → extract method description chunk
  "classref-item-separator" or next ".. _" → ready for next

SIGNAL_DESC:
  ".. _class_X_signal_NAME:" → extract signal description chunk
  "classref-item-separator" or next ".. _" → ready for next

ENUM_DESC:
  ".. _enum_X:" or "enum **Name**:" → extract enum chunk
  "classref-item-separator" or next ".. _" → ready for next

CONSTANT_DESC:
  ".. _class_X_constant_NAME:" → extract constant chunk
  "classref-item-separator" or next ".. _" → ready for next
```

### 3.3 Single-Pass Rationale

A single-pass state machine is the right choice because:
- The 457K-line file is processed in one linear scan (O(n) time, O(1) memory beyond chunk storage)
- Each class block is parsed immediately when its file boundary is detected — no need to store line ranges
- Tables (Properties/Methods) appear **before** their description blocks within the same class, so the state machine naturally transitions: class header → tables → descriptions
- Some classes have no tables at all (just descriptions) — the state machine handles this by going directly to the descriptions section
- The separation between table section and descriptions section is a `classref-section-separator`, which serves as a state transition trigger

The state machine design in Section 3.2 is inherently single-pass. Each line is visited exactly once, and state transitions occur as section markers are encountered.

---

## 4. Regex Patterns — Complete Catalog

### 4.1 File Boundaries

```python
# Match class file headers
FILE_HEADER_CLASS = re.compile(
    r'^## File: classes/class_([\w@]+)\.rst'
)

# Match non-class file headers (tutorials, getting_started)
FILE_HEADER_NON_CLASS = re.compile(
    r'^## File: (?!classes/)'
)

# Detect end of RST code block
RST_BLOCK_START = re.compile(r'^`````````?rst$')
RST_BLOCK_END = re.compile(r'^`````````?$')
```

### 4.2 Class Header

```python
# Class anchor: .. _class_Node3D:
CLASS_ANCHOR = re.compile(r'^\.\. _class_([\w@]+):$')

# Class name from ==== underline (backup)
CLASS_NAME_HEADER = re.compile(r'^([\w@]+)\s*$')  # used after anchor

# Inheritance line
INHERITS_LINE = re.compile(r'^\*\*Inherits:\*\*\s*(.+)$')

# Extract clean name from :ref:`name<link>`
REF_EXTRACT = re.compile(r':ref:`([^`<]+)<[^>]+>`')
```

### 4.3 RST Markup Cleanup

```python
# Strip RST markup for clean embedding text
RST_MARKUP_CLEANUP = [
    (re.compile(r':ref:`([^`<]+)<[^>]+>`'), r'\1'),      # :ref: links → just name
    (re.compile(r':doc:`([^`<]+)<[^>]+>`'), r'\1'),       # :doc: links → just name
    (re.compile(r'``([^`]+)``'), r'\1'),                   # ``literal`` → literal
    (re.compile(r'\*\*([^*]+)\*\*'), r'\1'),              # **bold** → bold
    (re.compile(r'\|\w+\|'), ''),                          # |void| → remove
    (re.compile(r'\\ '), ' '),                             # escaped spaces
    (re.compile(r'\\\('), '('),                            # escaped parens
    (re.compile(r'\\\)'), ')'),
    (re.compile(r':ref:`🔗<[^>]+>`'), ''),                # link icons → remove
]
```

### 4.4 Section Headers

```python
# Table section headers
SECTION_PROPERTIES_TABLE = re.compile(r'^Properties$')
SECTION_METHODS_TABLE = re.compile(r'^Methods$')
SECTION_SIGNALS_TABLE = re.compile(r'^Signals$')

# Description section markers
SECTION_DESCRIPTIONS_GROUP = re.compile(
    r'^\.\. rst-class:: classref-descriptions-group'
)
SECTION_SUBHEADER = re.compile(
    r'^(Signals|Enumerations|Constants|Property Descriptions|Method Descriptions)$'
)
```

### 4.5 Table Parsing

```python
# Table row (split by +---+ separators)
# Each row is: +----+----+----+  → split on +, trim each cell
TABLE_ROW = re.compile(r'^\+\-+')

# Extract :ref:`name<link>` from table cell
# Cell format: | :ref:`name<class_X_property_name>` |
TABLE_CELL_REF = re.compile(r':ref:`([^`]+)<class_\w+_(property|method|signal)_([^`]+)>`')

# Also match: | :ref:`Type<class_Type>` | :ref:`name<class_X_prop_name>` |
# → property name is in 2nd column; method name is in rightmost column
```

### 4.6 Description Blocks — Unified Anchor Patterns

All member types share a common anchor structure: `.. _class_ClassName_MEMBERTYPE_MemberName:`. A single unified regex captures the class name, member type, and member name:

```python
# Unified member anchor: captures class_name, member_type, member_name
# Handles ALL Godot RST anchor variants:
#   .. _class_Node3D_method_rotate_y:
#   .. _class_AABB_operator_neq_AABB:
#   .. _class_AABB_constructor_AABB:
#   .. _class_AnimationMixer_private_method__post_process_key_value:
#   .. _class_@GDScript_annotation_@abstract:
#   .. _class_Node3D_property_basis:
#   .. _class_Node3D_signal_visibility_changed:
#   .. _class_Node3D_constant_NOTIFICATION_TRANSFORM_CHANGED:
#   .. _class_AcceptDialog_theme_constant_buttons_min_height:
#   .. _class_Button_theme_color_font_color:
#   .. _class_Button_theme_style_normal:
MEMBER_ANCHOR = re.compile(
    r'^\.\. _class_([\w@.]+?)_'        # non-greedy class_name (fixes Bug 1)
    r'(private_method|theme_constant|theme_color|theme_icon|'
    r'theme_style|theme_font|theme_font_size|'  # all theme sub-types (longest first, fixes Bug 2)
    r'method|operator|constructor|'
    r'property|signal|constant|annotation)_'
    r'([\w@.]+):$'
)

# Enum anchor: .. _enum_Node3D_RotationEditMode:
# Also handles: .. _enum_@GlobalScope_Variant.Type:
ENUM_ANCHOR = re.compile(
    r'^\.\. _enum_([\w@.]+):$'
)

# Enum constant: .. _class_Node3D_constant_ROTATION_EDIT_MODE_EULER:
# (Already covered by MEMBER_ANCHOR with member_type='constant')

# Mapping: RST member type → chunk_type value
MEMBER_TYPE_TO_CHUNK_TYPE = {
    'method':           'method',
    'operator':         'operator',
    'constructor':      'constructor',
    'private_method':   'method',           # virtual methods → chunk_type 'method'
    'property':         'property',
    'signal':           'signal',
    'constant':         'constant',
    'annotation':       'annotation',       # @export, @abstract, etc.
    'theme_constant':   'theme_property',
    'theme_color':      'theme_property',
    'theme_icon':       'theme_property',
    'theme_style':      'theme_property',
    'theme_font':       'theme_property',
    'theme_font_size':  'theme_property',
}
```

**Member type summary and occurrence counts:**

| RST Member Type | chunk_type | Example Anchor | ~Count |
|----------------|-----------|---------------|--------|
| `method` | `method` | `.. _class_Node3D_method_rotate_y:` | ~20,000+ |
| `operator` | `operator` | `.. _class_AABB_operator_neq_AABB:` | ~351 |
| `constructor` | `constructor` | `.. _class_AABB_constructor_AABB:` | ~154 |
| `private_method` | `method` | `.. _class_AnimationMixer_private_method__post_process_key_value:` | ~varies |
| `property` | `property` | `.. _class_Node3D_property_basis:` | ~10,000+ |
| `signal` | `signal` | `.. _class_Node3D_signal_visibility_changed:` | ~1,500+ |
| `constant` | `constant` | `.. _class_Node3D_constant_NOTIFICATION_TRANSFORM_CHANGED:` | ~3,000+ |
| `annotation` | `annotation` | `.. _class_@GDScript_annotation_@abstract:` | ~36 |
| `theme_constant` | `theme_property` | `.. _class_AcceptDialog_theme_constant_buttons_min_height:` | ~540 |
| `theme_color` | `theme_property` | `.. _class_Button_theme_color_font_color:` | ~626 |
| `theme_icon` | `theme_property` | `.. _class_Button_theme_icon_arrow_down:` | ~552 |
| `theme_style` | `theme_property` | `.. _class_Button_theme_style_normal:` | ~439 |
| `theme_font` | `theme_property` | `.. _class_Button_theme_font_font:` | ~267 |
| `theme_font_size` | `theme_property` | `.. _class_Button_theme_font_size_font_size:` | ~27 |

**Key regex design decisions:**

- All name fields use `[\w@.]+` (not `\w+`) to handle `@` in class names (`@GDScript`), `@` in annotation names (`@abstract`), and `.` in enum names (`Variant.Type`)
- Member types are captured as a group, not hardcoded — a single pattern handles all 14 variants (9 member types + 5 additional theme sub-types)
- The `MEMBER_TYPE_TO_CHUNK_TYPE` mapping allows `private_method` anchors to produce `chunk_type='method'` (they're virtual methods) while `operator` and `constructor` produce distinct chunk types
- All 6 theme sub-type anchors (`theme_constant`, `theme_color`, `theme_icon`, `theme_style`, `theme_font`, `theme_font_size`) produce `chunk_type='theme_property'` to distinguish them from regular properties

**Signature extraction (per member type):**

```python
# Method/Operator/Constructor signature line:
#   |void| **rotate_y**\ (\ angle\: ... ) :ref:`🔗<...>`
#   |Vector3| **operator +**\ (\ other\: ... ) :ref:`🔗<...>`
#   **AABB**\ (\ ) :ref:`🔗<...>`  (constructor, no return type)
METHOD_SIGNATURE = re.compile(
    r'(?:[\w@.|]+)?\s*\*\*([\w@.]+)\*\*\s*\\?\s*'
    r'(.*?)(?:\s*:ref:`🔗|$)'
)

# Property signature line:
#   :ref:`Type<class_Type>` **name** :ref:`🔗<...>`
PROPERTY_SIGNATURE = re.compile(
    r':ref:`[^`]+`\s*\*\*([\w@.]+)\*\*'
)

# Signal signature line:
#   **signal_name**\ (\ params\ )
SIGNAL_SIGNATURE = re.compile(
    r'\*\*([\w@.]+)\*\*\s*\\?\s*\(([^)]*)\)'
)

# Constant signature line:
#   **NAME** = ``value``
CONSTANT_SIGNATURE = re.compile(
    r'\*\*([\w@.]+)\*\*\s*=\s*``([^`]*)``'
)

# Enum signature:
#   enum **Name**: or enum **Name**:
ENUM_SIGNATURE = re.compile(
    r'^enum\s+\*\*([\w@.]+)\*\*'
)

# Annotation signature line:
#   **@abstract**\ (\ ) :ref:`🔗<...>`
ANNOTATION_SIGNATURE = re.compile(
    r'\*\*([\w@.]+)\*\*\s*\\?\s*'
    r'(.*?)(?:\s*:ref:`🔗|$)'
)

# Theme property signature line:
#   **buttons_min_height** :ref:`🔗<...>`
THEME_PROPERTY_SIGNATURE = re.compile(
    r'\*\*([\w@.]+)\*\*'
)
```

**Note on `\w+` vs `[\w@.]+`:** All regex patterns that capture names (class name, method name, property name, signal name, constant name, enum name, annotation name, and theme property name) use `[\w@.]+` instead of `\w+`. This is essential for:
- `@GDScript` class names (the `@` prefix)
- `@abstract`, `@export` annotation names  
- `Variant.Type` enum names (the `.` separator)
- `_post_process_key_value` — underscores in virtual method names (already covered by `\w`, but documented for clarity)

### 4.7 Item Separators

```python
# End of description block
ITEM_SEPARATOR = re.compile(r'^\.\. rst-class:: classref-item-separator$')
SECTION_SEPARATOR = re.compile(r'^\.\. rst-class:: classref-section-separator$')
```

---

## 5. Chunk Generation Mapping

| RST Element | chunk_type | chunk_id pattern | What goes in `text` |
|------------|-----------|-----------------|-------------------|
| Class overview | `class` | `Classname::class` | Cleaned class name + inherits chain + description |
| Method | `method` | `Classname::method::methodname` | Cleaned signature + description text |
| Operator | `operator` | `Classname::operator::operatorname` | Cleaned signature + description text (~351) |
| Constructor | `constructor` | `Classname::constructor::constructorname` | Cleaned signature + description text (~154) |
| Property | `property` | `Classname::property::propname` | Cleaned signature + description text |
| Signal | `signal` | `Classname::signal::signalname` | Cleaned signature + description text |
| Enum | `enum` | `Classname::enum::enumname` | Enum name + constants + descriptions |
| Constant | `constant` | `Classname::constant::constname` | Name + value + description text |
| Annotation | `annotation` | `Classname::annotation::annotationname` | Annotation name + description text (~36) |
| Theme Property | `theme_property` | `Classname::theme_property::propname` | Name + type + description text (~635) |

**Note on `private_method`:** Virtual methods (marked by `_private_method_` in RST anchors) map to `chunk_type='method'`. They use the same extraction logic as regular methods. The `private` prefix is internal RST convention; the chunk output doesn't distinguish them.

### 5.1 Text Cleaning for Embedding

All `text` fields are stripped of RST markup before embedding:
- `:ref:`text<link>`` → `text`
- `:doc:`text<link>`` → `text`
- `**bold**` → `bold`
- `` ``literal`` `` → `literal`
- `|void|`, `|const|`, `|vararg|` → removed
- `\ ` escaped spaces → spaces
- ````` ``value`` ````` → `value`
- `.. rst-class:: *` directives → removed
- `🔗` icons → removed

### 5.2 Class Chunk Example

```python
Chunk(
    chunk_id="Node3D::class",
    domain="godot",
    text="Class: Node3D extends Node → Object\n\n"
         "The Node3D node is the base representation of a node in 3D space. "
         "All other 3D nodes inherit from this class.\n\n"
         "Affine operations (translation, rotation, scale) are calculated in "
         "the coordinate system relative to the parent...",
    source_type="repo",
    chunk_type="class",
    class_name="Node3D",
    name="Node3D",
    inherits_from=["Node", "Object"],
    docstring="The Node3D node is the base representation..."[:500],
    source_file="godot-docs-reference-packed.md",
    line_start=218375,
    line_end=218407,
)
```

### 5.3 Method Chunk Example

```python
Chunk(
    chunk_id="Node3D::method::rotate_y",
    domain="godot",
    text="Method: Node3D.rotate_y\n"
         "Signature: void rotate_y(angle: float)\n"
         "Inherits: Node → Object\n\n"
         "Rotates this node's basis around the Y axis by the given angle, "
         "in radians. This operation is calculated in parent space (relative "
         "to the parent) and preserves the position.",
    source_type="repo",
    chunk_type="method",
    class_name="Node3D",
    name="rotate_y",
    signature="void rotate_y(angle: float)",
    inherits_from=["Node", "Object"],
    docstring="Rotates this node's basis around the Y axis..."[:500],
    source_file="godot-docs-reference-packed.md",
    line_start=219284,
    line_end=219293,
)
```

### 5.4 Property Chunk Example

```python
Chunk(
    chunk_id="Node3D::property::basis",
    domain="godot",
    text="Property: Node3D.basis\n"
         "Type: Basis\n"
         "Setter: set_basis(value: Basis)\n"
         "Getter: get_basis()\n"
         "Inherits: Node → Object\n\n"
         "Basis of the transform property. Represents the rotation, scale, "
         "and shear of this node in parent space (relative to the parent node).",
    source_type="repo",
    chunk_type="property",
    class_name="Node3D",
    name="basis",
    signature="Basis basis",
    inherits_from=["Node", "Object"],
    docstring="Basis of the transform property..."[:500],
    source_file="godot-docs-reference-packed.md",
    line_start=218662,
    line_end=218676,
)
```

### 5.5 Constant Chunk Example

```python
Chunk(
    chunk_id="Node3D::constant::NOTIFICATION_TRANSFORM_CHANGED",
    domain="godot",
    text="Constant: Node3D.NOTIFICATION_TRANSFORM_CHANGED = 2000\n"
         "Inherits: Node → Object\n\n"
         "Notification received when this node's global_transform changes, "
         "if is_transform_notification_enabled() is true.",
    source_type="repo",
    chunk_type="constant",
    class_name="Node3D",
    name="NOTIFICATION_TRANSFORM_CHANGED",
    signature="NOTIFICATION_TRANSFORM_CHANGED = 2000",
    inherits_from=["Node", "Object"],
    docstring="Notification received when this node's..."[:500],
    source_file="godot-docs-reference-packed.md",
    line_start=...,
    line_end=...,
)
```

---

## 6. Parser Architecture — `Parser.parse()` Method

### 6.1 Method Signature (unchanged)

```python
def parse(self, file_path: str, content: str) -> list[Chunk]:
```

- `file_path`: path to the packed `.md` file
- `content`: entire file content as a single string
- Returns: `list[Chunk]` — structured chunks for class files, empty list for non-class content (triggering fallback in `embed_index.py`)

### 6.2 Main Algorithm (Pseudocode)

```python
class Parser(DomainParser):
    source_type_name = "rst-godot"

    def parse(self, file_path: str, content: str) -> list[Chunk]:
        chunks = []
        lines = content.splitlines()
        i = 0
        
        while i < len(lines):
            # Look for class file boundary
            m = FILE_HEADER_CLASS.match(lines[i])
            if not m:
                i += 1
                continue
            
            class_name = m.group(1)
            i += 1
            
            # Find the RST content block start
            while i < len(lines) and not RST_BLOCK_START.match(lines[i]):
                i += 1
            i += 1  # skip ``````rst
            
            # Parse this class's RST content
            class_chunks, i = self._parse_class_block(
                lines, i, class_name, file_path
            )
            chunks.extend(class_chunks)
            # i now points past the class block end
        
        return chunks
```

### 6.3 `_parse_class_block()` — The Core

```python
def _parse_class_block(
    self, lines: list[str], start: int, class_name: str, file_path: str
) -> tuple[list[Chunk], int]:
    """
    Parse a single class RST block from `start` line index.
    
    Returns:
        (chunks, next_line) where next_line is after the block.
    
    State machine within a class block:
    1. Find class anchor + header → class overview chunk
    2. Parse tables section (Properties, Methods, Signals) → collect names
    3. Parse descriptions section → full chunks with docstrings
    """
    
    class_chunks = []
    inherits = None
    description_lines = []
    in_class_header = False
    in_properties_table = False
    in_methods_table = False
    in_signals_table = False
    in_descriptions = False
    
    # Collections for matching tables to descriptions later
    table_properties: list[str] = []
    table_methods: dict[str, str] = {}  # name → signature
    table_signals: list[str] = []
    
    current_desc_type = None  # "properties" | "methods" | "signals" | "enums" | "constants"
    current_desc_lines: list[str] = []
    current_desc_name = None
    current_desc_signature = None
    
    i = start
    while i < len(lines):
        line = lines[i]
        
        # End of RST code block
        if RST_BLOCK_END.match(line):
            i += 1
            break
        
        # Class anchor → start class header
        m = CLASS_ANCHOR.match(line)
        if m and not in_class_header:
            in_class_header = True
            i += 1
            continue
        
        # Inheritance line within class header
        if in_class_header:
            inherits_match = INHERITS_LINE.match(line)
            if inherits_match:
                inherits = self._extract_ref_names(inherits_match.group(1))
                i += 1
                continue
            
            # Accumulate description text
            if line.strip() and not line.startswith('.. '):
                description_lines.append(line)
            
            # End of header when we hit Properties/Methods/Signals header
            if any(h in line for h in ['Properties', 'Methods', 'Signals', 'Enumerations']):
                # Flush class overview chunk
                class_chunks.append(self._make_class_chunk(
                    class_name, inherits, description_lines, file_path, i
                ))
                in_class_header = False
                description_lines = []
        
        # Section headers for tables
        if SECTION_PROPERTIES_TABLE.search(line) and 'Properties' in line and '--------' not in line:
            in_properties_table = True
            in_methods_table = False
            in_signals_table = False
        
        if SECTION_METHODS_TABLE.search(line) and 'Methods' in line and '--------' not in line:
            in_properties_table = False
            in_methods_table = True
            in_signals_table = False
        
        # Table rows
        if in_properties_table and self._is_table_row(line):
            props = self._extract_property_names_from_row(line)
            table_properties.extend(props)
        
        if in_methods_table and self._is_table_row(line):
            methods = self._extract_methods_from_row(line)
            table_methods.update(methods)
        
        # End of a table (blank line after table)
        if (in_properties_table or in_methods_table) and not line.strip():
            in_properties_table = False
            in_methods_table = False
        
        # Descriptions group
        m = SECTION_DESCRIPTIONS_GROUP.match(line)
        if m:
            in_descriptions = True
            in_properties_table = False
            in_methods_table = False
            i += 1
            continue
        
        # Sub-header within descriptions
        if in_descriptions and SECTION_SUBHEADER.match(line):
            # Flush previous description if any
            if current_desc_name and current_desc_type:
                chunk = self._make_description_chunk(
                    current_desc_type, class_name, current_desc_name,
                    current_desc_signature, inherits, current_desc_lines,
                    file_path, i
                )
                if chunk:
                    class_chunks.append(chunk)
            
            sub = SECTION_SUBHEADER.match(line)
            section_name = sub.group(1)
            current_desc_type = {
                'Property Descriptions': 'property',
                'Method Descriptions': 'method',
                'Signals': 'signal',
                'Enumerations': 'enum',
                'Constants': 'constant',
            }.get(section_name)
            
            current_desc_lines = []
            current_desc_name = None
            current_desc_signature = None
            i += 1
            continue
        
        # Description anchors → extract name + signature
        if in_descriptions:
            # Unified MEMBER_ANCHOR (matches method, operator, constructor, private_method,
            # property, signal, constant, annotation, and all 6 theme sub-types)
            m = MEMBER_ANCHOR.match(line)
            if m:
                if current_desc_name:
                    # Flush previous
                    chunk = self._make_description_chunk(...)
                    if chunk: class_chunks.append(chunk)
                
                member_type = m.group(2)
                current_desc_name = m.group(3)
                chunk_type = MEMBER_TYPE_TO_CHUNK_TYPE.get(member_type, 'fallback')
                i += 1
                # Next line(s) have the signature
                if i < len(lines):
                    sig_line = lines[i]
                    # Select signature regex based on chunk_type
                    if chunk_type in ('method', 'operator', 'constructor'):
                        sig_m = METHOD_SIGNATURE.search(sig_line)
                        if sig_m:
                            current_desc_signature = f"{sig_m.group(1)}{sig_m.group(2)}"
                    elif chunk_type == 'property' or chunk_type == 'theme_property':
                        sig_m = PROPERTY_SIGNATURE.search(sig_line) or THEME_PROPERTY_SIGNATURE.search(sig_line)
                        if sig_m:
                            current_desc_signature = sig_m.group(1)
                    elif chunk_type == 'signal':
                        sig_m = SIGNAL_SIGNATURE.search(sig_line)
                        if sig_m:
                            current_desc_signature = f"{sig_m.group(1)}{sig_m.group(2)}"
                    elif chunk_type == 'constant':
                        sig_m = CONSTANT_SIGNATURE.search(sig_line)
                        if sig_m:
                            current_desc_signature = f"{sig_m.group(1)} = {sig_m.group(2)}"
                    elif chunk_type == 'annotation':
                        sig_m = ANNOTATION_SIGNATURE.search(sig_line)
                        if sig_m:
                            current_desc_signature = f"{sig_m.group(1)}{sig_m.group(2)}"
                    current_chunk_type = chunk_type
                continue
            
            # Accumulate description text (skip directive lines)
            if line.strip() and not line.startswith('.. '):
                cleaned = self._clean_rst_text(line)
                current_desc_lines.append(cleaned)
        
        i += 1
    
    # Flush final description
    ...
    
    return class_chunks, i
```

### 6.4 Table Row Parsing

```python
def _is_table_row(self, line: str) -> bool:
    """Check if line is an RST table row."""
    return bool(re.match(r'^\|\s', line))

def _extract_property_names_from_row(self, line: str) -> list[str]:
    """
    Property table: Column 2 has :ref:`name<link>`.
    Format: | :ref:`Type<class_Type>` | :ref:`propname<class_Class_property_propname>` |
    """
    cells = [c.strip() for c in line.split('|')]
    # Property name is in cell 2 (index 1, since split on | gives empty first)
    # Actually: "| col1 | col2 |" → split gives ['', 'col1', 'col2', '']
    names = []
    for cell in cells:
        for ref in REF_EXTRACT.findall(cell):
            # Check if it looks like a property ref
            if '_property_' in cell:
                names.append(ref)
    return names

def _extract_methods_from_row(self, line: str) -> dict[str, str]:
    """
    Method table: Rightmost cell has :ref:`name<link>` and signature.
    Returns {method_name: signature_text}.
    """
    cells = [c.strip() for c in line.split('|')]
    # Last non-empty cell
    methods = {}
    for cell in reversed(cells):
        if not cell:
            continue
        # Extract method name from :ref: pattern
        refs = REF_EXTRACT.findall(cell)
        if refs:
            name = refs[-1]  # usually the last ref
            # Clean signature
            sig = self._clean_rst_text(cell)
            methods[name] = sig
        break
    return methods
```

### 6.5 RST Text Cleaning

```python
def _clean_rst_text(self, text: str) -> str:
    """Strip RST markup for clean embedding text."""
    # Replace :ref:`text<link>` → text
    text = re.sub(r':ref:`([^`<]+)<[^>]+>`', r'\1', text)
    # Replace :doc:`text<link>` → text
    text = re.sub(r':doc:`([^`<]+)<[^>]+>`', r'\1', text)
    # Replace ``literal`` → literal
    text = re.sub(r'``([^`]+)``', r'\1', text)
    # Replace **bold** → bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    # Remove |type| markers
    text = re.sub(r'\|(\w+)\|', '', text)
    # Remove escaped spaces
    text = text.replace('\\ ', ' ')
    # Remove escaped parens
    text = text.replace('\\(', '(').replace('\\)', ')')
    # Remove link icons
    text = re.sub(r':ref:`🔗<[^>]+>`', '', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def _extract_ref_names(self, inherits_text: str) -> list[str]:
    """Extract class names from **Inherits:** line.
    
    Input: ':ref:`Node<class_Node>` **<** :ref:`Object<class_Object>`'
    Output: ['Node', 'Object']
    """
    return REF_EXTRACT.findall(inherits_text)
```

---

## 7. Fallback Behavior for Non-Class Content

### 7.1 Parser is Called for ALL Source Files

The parser's `parse()` method is called for **all 4 source files** in the Godot domain, not just the reference:

| Source File | Content Type | Parser Behavior |
|------------|-------------|----------------|
| `godot-docs-reference-packed.md` | 1,078 class RST files | Parses structured chunks |
| `godot-demos-packed.md` | Demo project source code | Returns `[]` → fallback |
| `godot-docs-3d-packed.md` | Tutorials / guides | Returns `[]` → fallback |
| `test-src.md` | Test RST content | Returns `[]` → fallback |

### 7.2 Detection Logic

When the packed file's `## File:` header doesn't match `classes/class_*.rst`, the parser returns an empty list:

```python
def parse(self, file_path: str, content: str) -> list[Chunk]:
    chunks = []
    
    # Quick check: does this file contain class RST content?
    # Check first 1000 characters for 'classes/class_' pattern
    if 'classes/class_' not in content[:1000]:
        return []  # Empty → embed_index.py uses fallback_chunk()
    
    # ... proceed with class parsing
```

**Important:** The `content[:1000]` check is a fast heuristic, not an exact match. The repomix-packed file header format is:

```
## File: classes/class_node3d.rst
``````````rst
```

This pattern reliably appears within the first 1000 characters of any class file. Non-class files (demos, tutorials, test-src) lack this pattern and correctly return `[]`.

### 7.3 Caller Contract (embed_index.py)

The `embed_index.py` caller already handles empty return:
```python
parsed = parser.parse(str(file), content)
if parsed:
    # Use structured chunks for ChromaDB indexing
    ...
else:
    # Fallback chunking via sliding windows
    fallback = fallback_chunk(content, ...)
```

**No change needed in embed_index.py** — the existing contract works. The new parser simply returns `[]` for non-class files, and the fallback mechanism handles them correctly.

---

## 8. Testing Strategy

### 8.1 Unit Tests (Manual Validation — Test Script)

Create a standalone test script at `domains/godot/test_parser.py` (not committed, gitignored):

```python
#!/usr/bin/env python3
"""Manual test harness for Godot RST parser."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

from domains.godot.parser import Parser

# ── Test 1: Node3D (complete class with properties, methods, signals, enums, constants) ──

def test_node3d():
    source = Path("domains/godot/sources/godot-docs-reference-packed.md")
    content = source.read_text()
    
    # Extract just the Node3D section
    start = content.find("class_node3d.rst")
    end = content.find("## File:", start + 100)
    if end == -1:
        end = len(content)
    node3d_content = content[start:end]
    
    parser = Parser()
    chunks = parser.parse(str(source), node3d_content)
    
    print(f"Node3D chunks: {len(chunks)}")
    
    # Verify class chunk
    class_chunks = [c for c in chunks if c.chunk_type == "class"]
    assert len(class_chunks) == 1, f"Expected 1 class chunk, got {len(class_chunks)}"
    assert class_chunks[0].class_name == "Node3D"
    assert class_chunks[0].inherits_from == ["Node", "Object"]
    print("  ✅ Class chunk OK")
    
    # Verify methods
    method_chunks = [c for c in chunks if c.chunk_type == "method"]
    assert len(method_chunks) >= 30, f"Expected >= 30 methods, got {len(method_chunks)}"
    rotate_y = [c for c in method_chunks if c.name == "rotate_y"]
    assert len(rotate_y) == 1
    assert "Rotates this node" in rotate_y[0].docstring
    print(f"  ✅ {len(method_chunks)} methods OK")
    
    # Verify properties
    prop_chunks = [c for c in chunks if c.chunk_type == "property"]
    assert len(prop_chunks) >= 15, f"Expected >= 15 properties, got {len(prop_chunks)}"
    basis = [c for c in prop_chunks if c.name == "basis"]
    assert len(basis) == 1
    print(f"  ✅ {len(prop_chunks)} properties OK")
    
    # Verify signals
    signal_chunks = [c for c in chunks if c.chunk_type == "signal"]
    assert len(signal_chunks) >= 1, f"Expected >= 1 signal, got {len(signal_chunks)}"
    print(f"  ✅ {len(signal_chunks)} signals OK")
    
    # Verify enums + constants
    enum_chunks = [c for c in chunks if c.chunk_type == "enum"]
    constant_chunks = [c for c in chunks if c.chunk_type == "constant"]
    print(f"  ✅ {len(enum_chunks)} enums, {len(constant_chunks)} constants")

# ── Test 2: @GDScript (special chars in name, constants, no properties/signals) ──

def test_gdscript():
    source = Path("domains/godot/sources/godot-docs-reference-packed.md")
    content = source.read_text()
    
    start = content.find("class_@gdscript.rst")
    end = content.find("## File:", start + 100)
    gdscript_content = content[start:end]
    
    parser = Parser()
    chunks = parser.parse(str(source), gdscript_content)
    
    assert len(chunks) > 0
    class_chunks = [c for c in chunks if c.chunk_type == "class"]
    assert len(class_chunks) == 1
    assert class_chunks[0].class_name == "@GDScript"
    print(f"  ✅ @GDScript: {len(chunks)} chunks")

# ── Test 3: Inheritance chain extraction ──

def test_inherits():
    text = "**Inherits:** :ref:`Node<class_Node>` **<** :ref:`Object<class_Object>`"
    parser = Parser()
    names = parser._extract_ref_names(text)
    assert names == ["Node", "Object"], f"Expected ['Node', 'Object'], got {names}"
    print("  ✅ Inheritance extraction OK")

# ── Test 4: RST text cleaning ──

def test_cleaning():
    parser = Parser()
    
    assert parser._clean_rst_text(":ref:`Node<class_Node>`") == "Node"
    assert parser._clean_rst_text("**bold** text") == "bold text"
    assert parser._clean_rst_text("``literal`` value") == "literal value"
    assert parser._clean_rst_text("|void|") == ""
    assert parser._clean_rst_text(":ref:`🔗<link>`") == ""
    print("  ✅ RST cleaning OK")

# ── Test 5: Non-class file returns empty ──

def test_tutorial():
    source = Path("domains/godot/sources/godot-docs-reference-packed.md")
    content = source.read_text()
    
    start = content.find("getting_started/first_2d_game/01")
    end = content.find("## File:", start + 100)
    tutorial_content = content[start:end]
    
    parser = Parser()
    chunks = parser.parse(str(source), tutorial_content)
    
    assert len(chunks) == 0, f"Tutorial should return 0 chunks, got {len(chunks)}"
    print("  ✅ Tutorial fallback OK")

# ── Test 6: AABB (operators + constructors, no signals) ──

def test_aabb():
    source = Path("domains/godot/sources/godot-docs-reference-packed.md")
    content = source.read_text()

    start = content.find("class_aabb.rst")
    end = content.find("## File:", start + 100)
    if end == -1:
        end = len(content)
    aabb_content = content[start:end]

    parser = Parser()
    chunks = parser.parse(str(source), aabb_content)

    print(f"AABB chunks: {len(chunks)}")

    # Verify class chunk
    class_chunks = [c for c in chunks if c.chunk_type == "class"]
    assert len(class_chunks) == 1, f"Expected 1 class chunk, got {len(class_chunks)}"
    assert class_chunks[0].class_name == "AABB"
    print("  ✅ Class chunk OK")

    # Verify constructors
    constructor_chunks = [c for c in chunks if c.chunk_type == "constructor"]
    assert len(constructor_chunks) >= 1, f"Expected >= 1 constructor, got {len(constructor_chunks)}"
    print(f"  ✅ {len(constructor_chunks)} constructors")

    # Verify operators
    operator_chunks = [c for c in chunks if c.chunk_type == "operator"]
    assert len(operator_chunks) >= 1, f"Expected >= 1 operator, got {len(operator_chunks)}"
    print(f"  ✅ {len(operator_chunks)} operators")

    # AABB has no signals
    signal_chunks = [c for c in chunks if c.chunk_type == "signal"]
    assert len(signal_chunks) == 0, f"AABB should have 0 signals, got {len(signal_chunks)}"
    print("  ✅ No signals (as expected)")

# ── Test 7: AnimationMixer (virtual methods with _private_method_) ──

def test_animation_mixer():
    source = Path("domains/godot/sources/godot-docs-reference-packed.md")
    content = source.read_text()

    start = content.find("class_animationmixer.rst")
    end = content.find("## File:", start + 100)
    if end == -1:
        end = len(content)
    am_content = content[start:end]

    parser = Parser()
    chunks = parser.parse(str(source), am_content)

    print(f"AnimationMixer chunks: {len(chunks)}")

    # Verify class chunk
    class_chunks = [c for c in chunks if c.chunk_type == "class"]
    assert len(class_chunks) == 1
    assert class_chunks[0].class_name == "AnimationMixer"

    # Method chunks should include virtual methods (from _private_method_ anchors)
    method_chunks = [c for c in chunks if c.chunk_type == "method"]
    # _post_process_key_value is a common virtual method
    ppkv = [c for c in method_chunks if c.name == "_post_process_key_value"]
    if ppkv:
        print(f"  ✅ _post_process_key_value virtual method found (1 of {len(method_chunks)} methods)")
    else:
        print(f"  ⚠️ _post_process_key_value not found, but {len(method_chunks)} methods parsed")
    print("  ✅ AnimationMixer OK")

# ── Test 8: AcceptDialog (theme properties) ──

def test_accept_dialog():
    source = Path("domains/godot/sources/godot-docs-reference-packed.md")
    content = source.read_text()

    start = content.find("class_acceptdialog.rst")
    end = content.find("## File:", start + 100)
    if end == -1:
        end = len(content)
    ad_content = content[start:end]

    parser = Parser()
    chunks = parser.parse(str(source), ad_content)

    print(f"AcceptDialog chunks: {len(chunks)}")

    # Verify theme properties
    theme_chunks = [c for c in chunks if c.chunk_type == "theme_property"]
    # buttons_min_height is a known theme constant
    bmh = [c for c in theme_chunks if c.name == "buttons_min_height"]
    if bmh:
        print(f"  ✅ buttons_min_height theme property found (1 of {len(theme_chunks)} theme properties)")
    else:
        print(f"  ⚠️ buttons_min_height not found, but {len(theme_chunks)} theme properties parsed")
    print("  ✅ AcceptDialog OK")

# ── Test 8b: Button (theme_color, theme_style, theme_font, theme_icon sub-types) ──

def test_button_themes():
    source = Path("domains/godot/sources/godot-docs-reference-packed.md")
    content = source.read_text()

    start = content.find("class_button.rst")
    end = content.find("## File:", start + 100)
    if end == -1:
        end = len(content)
    btn_content = content[start:end]

    parser = Parser()
    chunks = parser.parse(str(source), btn_content)

    print(f"Button chunks: {len(chunks)}")

    # Verify theme properties of ALL sub-types
    theme_chunks = [c for c in chunks if c.chunk_type == "theme_property"]

    # theme_color test
    font_color = [c for c in theme_chunks if "font_color" in c.name]
    if font_color:
        print(f"  ✅ font_color theme_color found (1 of {len(theme_chunks)} theme properties)")
    else:
        print(f"  ⚠️ font_color not found, but {len(theme_chunks)} theme properties parsed")

    # theme_style test
    normal_style = [c for c in theme_chunks if c.name == "normal"]
    if normal_style:
        print(f"  ✅ normal theme_style found")
    else:
        print(f"  ⚠️ normal theme_style not found")

    # theme_font test
    font_prop = [c for c in theme_chunks if c.name == "font"]
    if font_prop:
        print(f"  ✅ font theme_font found")
    else:
        print(f"  ⚠️ font theme_font not found")

    # theme_icon test
    icon_prop = [c for c in theme_chunks if "arrow" in c.name.lower()]
    if icon_prop:
        print(f"  ✅ arrow theme_icon found")
    else:
        print(f"  ⚠️ arrow theme_icon not found")

    print("  ✅ Button themes OK")

# ── Test 9: @GlobalScope (enum with . in name, @ in class name) ──

def test_globalscope():
    source = Path("domains/godot/sources/godot-docs-reference-packed.md")
    content = source.read_text()

    start = content.find("class_@globalscope.rst")
    end = content.find("## File:", start + 100)
    if end == -1:
        end = len(content)
    gs_content = content[start:end]

    parser = Parser()
    chunks = parser.parse(str(source), gs_content)

    print(f"@GlobalScope chunks: {len(chunks)}")

    # Verify class chunk handles @ in name
    class_chunks = [c for c in chunks if c.chunk_type == "class"]
    assert len(class_chunks) == 1
    assert class_chunks[0].class_name == "@GlobalScope"
    print("  ✅ @GlobalScope class chunk OK")

    # Verify enums (Variant.Type has . in name)
    enum_chunks = [c for c in chunks if c.chunk_type == "enum"]
    variant_type = [c for c in enum_chunks if "Variant" in c.name and "Type" in c.name]
    if variant_type:
        print(f"  ✅ Variant.Type enum found (1 of {len(enum_chunks)} enums)")
    else:
        print(f"  ⚠️ Variant.Type not found, but {len(enum_chunks)} enums parsed")
    print("  ✅ @GlobalScope OK")

# ── Test 10: All 4 source files parse correctly ──

def test_all_source_files():
    """Verify that all 4 source files are handled correctly."""
    source_dir = Path("domains/godot/sources/")
    source_files = sorted(source_dir.glob("*.md"))
    
    parser = Parser()
    
    for sf in source_files:
        content = sf.read_text(encoding='utf-8')
        chunks = parser.parse(str(sf), content)
        
        if 'godot-docs-reference-packed.md' in str(sf):
            # Reference file: should have structured chunks
            assert len(chunks) > 0, f"Reference file returned 0 chunks!"
            class_count = len([c for c in chunks if c.chunk_type == 'class'])
            assert class_count > 0, f"Reference file has no class chunks"
            print(f"  ✅ {sf.name}: {len(chunks)} chunks ({class_count} classes)")
        elif 'godot-demos-packed.md' in str(sf):
            # Demo file: non-RST, should return empty (fallback)
            if len(chunks) == 0:
                print(f"  ✅ {sf.name}: empty (fallback chunking)")
            else:
                print(f"  ⚠️ {sf.name}: {len(chunks)} chunks (unexpected, but may be OK)")
        elif 'godot-docs-3d-packed.md' in str(sf):
            # 3D tutorials: non-RST, should return empty
            if len(chunks) == 0:
                print(f"  ✅ {sf.name}: empty (fallback chunking)")
            else:
                print(f"  ⚠️ {sf.name}: {len(chunks)} chunks (unexpected)")
        elif 'test-src.md' in str(sf):
            # Test source: should return empty (no class content)
            if len(chunks) == 0:
                print(f"  ✅ {sf.name}: empty (fallback chunking)")
            else:
                print(f"  ⚠️ {sf.name}: {len(chunks)} chunks (but test file — OK either way)")

if __name__ == "__main__":
    print("=== Godot RST Parser Tests ===\n")
    test_inherits()
    test_cleaning()
    test_node3d()
    test_gdscript()
    test_tutorial()
    test_aabb()
    test_animation_mixer()
    test_accept_dialog()
    test_button_themes()
    test_globalscope()
    test_all_source_files()
    print("\n✅ All tests passed!")
```

### 8.2 Integration Test

After rewriting the parser, run a full index build:

```bash
# Build index with new parser
python scripts/embed_index.py --domain godot
```

**Expected:** 
- Structured chunks from all 1,078 class files (not 0 as before)
- Log shows: `[INFO] Parser 'rst-godot': NNN structured chunks from godot-docs-reference-packed.md`
- Zero fallback chunks for the reference file

### 8.3 Search Quality Smoke Test

```bash
# Hybrid search with structured results
python scripts/hybrid_search.py --domain godot --query "rotate Node3D around Y axis" --json
```

**Expected:** Results show `chunk_type: method`, `class_name: Node3D`, `name: rotate_y`.

---

## 9. Implementation Steps (Bite-Sized Diffs)

### Step 1: Rewrite `domains/godot/parser.py`

Complete replacement. The file goes from 237 lines (current) to ~450-500 lines.

**Key sections to implement in order:**
1. Regex patterns (class-level constants) — ~40 lines
2. `parse()` method — file boundary scan + class block dispatch — ~30 lines
3. `_parse_class_block()` — state machine — ~200 lines  
4. `_make_class_chunk()`, `_make_method_chunk()`, etc. — ~50 lines
5. `_clean_rst_text()`, `_extract_ref_names()` — ~30 lines
6. `_is_table_row()`, `_extract_property_names_from_row()`, `_extract_methods_from_row()` — ~50 lines

### Step 2: Run Tests

```bash
# Syntax check
python3 -m py_compile domains/godot/parser.py

# Unit tests
python3 domains/godot/test_parser.py
```

### Step 3: Full Index Rebuild

```bash
python scripts/embed_index.py --domain godot
```

Verify: structured chunks count > 0 in log output.

### Step 4: Update Known Issues

Remove LIM-002 from `docs/ai/known-issues.md`:

```markdown
- **LIM-002:** ❌ ~~Godot-Parser produziert aktuell 0 strukturierte Chunks~~ → Behoben 2026-06-10 (RST-Parser-Rewrite)
```

### Step 5: Commit

```bash
git add domains/godot/parser.py docs/ai/known-issues.md
git commit -m "feat(godot): rewrite RST parser for real Godot doc format

Replace regex-based parser with state machine that handles the actual
Godot RST structure: class anchors, RST tables for properties/methods,
per-member description blocks, signals, enums, and constants.

- Parses 1,078 class files from the packed godot-docs-reference file
- Extracts inheritance chains from **Inherits:** lines
- Cleans :ref:, :doc:, **bold**, ``literal`` markup for clean embeddings
- Non-class files (tutorials) correctly return empty for fallback chunking
- Fixes LIM-002 (0 structured chunks limitation)"
```

---

## 10. Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Edge cases in table parsing (e.g., classes with no Properties table, @GDScript) | Medium | Test against @GDScript (no properties/signals), Node3D (full-featured), AABB (simple) |
| Performance: 457K lines single-pass | Low | Single-pass with early exit for non-class files. 1,078 classes × avg 400 lines = ~430K lines parsed, roughly O(n) |
| Rebuild cost | Low | Full index rebuild ≈ 3-5 minutes on M-series Mac. Acceptable for one-time migration |
| Inheritance parsing failure for unusual chains | Low | Fall back to None if regex doesn't match. Class chunk is still valid without inheritance |
| @ prefix and . in names (e.g., @GDScript, @GlobalScope, Variant.Type) | Low | All name-capturing regex groups use `[\w@.]+` to handle @ and . characters |

## 11. Acceptance Criteria

- [ ] Parser produces > 0 structured chunks (current: 0)
- [ ] Node3D test: class chunk with inherits `["Node", "Object"]`
- [ ] Node3D test: ≥ 30 method chunks extracted  
- [ ] Node3D test: ≥ 15 property chunks extracted
- [ ] Node3D test: ≥ 1 signal chunk extracted
- [ ] @GDScript test: handles special characters in class name
- [ ] Tutorial files return empty list (fallback kicks in)
- [ ] `python -m py_compile domains/godot/parser.py` passes
- [ ] `python scripts/embed_index.py --domain godot` succeeds
- [ ] LIM-002 removed from known-issues.md
- [ ] AABB: ≥ 1 operator chunk extracted (e.g., `operator !=`)
- [ ] AABB: ≥ 1 constructor chunk extracted (e.g., `AABB()`)
- [ ] @GDScript: ≥ 1 annotation chunk extracted (e.g., `@abstract`, `@export`)
- [ ] Button: ≥ 1 theme_property chunk for each sub-type (theme_constant, theme_color, theme_icon, theme_style, theme_font, theme_font_size)
