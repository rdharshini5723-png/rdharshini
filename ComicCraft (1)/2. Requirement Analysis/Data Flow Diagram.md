**Team ID:** SWTID-2026-9211  
**Project Title:** ComicCraft - AI Comic Story Creator using Gemini Models  
**Team Size:** 5  
**Team Leader:** Dharshini  
**Team Members:** Pavi, J. Sakthi Devathai, Pavithra Mahadevan, Bhuvaneshwari

---

# Data Flow Diagram

## Level 0 (Context Diagram)

```
+------+   Story idea, style, characters   +-----------------------+   Prompts   +----------------+
| User | --------------------------------> |   ComicCraft System   | ----------> | Gemini Models  |
|      | <-------------------------------- |                       | <---------- | (Text + Image) |
+------+     Final comic (PDF / PNG)        +-----------------------+  Script &   +----------------+
                                                                       Images
```

## Level 1

```
User -> [1.0 Collect Story Input] -> [2.0 Generate Panel Script] -> [3.0 Build Character Sheet]
     -> [4.0 Generate Panel Images] -> [5.0 Add Speech Bubbles] -> [6.0 Compose Comic Page]
     -> [7.0 Export PDF / PNG] -> User
```

| Process ID | Process Name | Input | Output | Data Store / External Entity |
|------------|--------------|-------|--------|------------------------------|
| 1.0 | Collect Story Input | Story idea, genre, style, panel count | Validated request | User (External Entity) |
| 2.0 | Generate Panel Script | Validated request | Panel script (JSON) | Gemini Text Model |
| 3.0 | Build Character Sheet | Panel script | Fixed character descriptions | Session State |
| 4.0 | Generate Panel Images | Scene prompt + character sheet + style | Panel images | Gemini Image Model |
| 5.0 | Add Speech Bubbles | Panel images + dialogue | Lettered panels | Pillow Library |
| 6.0 | Compose Comic Page | Lettered panels | Comic page layout | Session State |
| 7.0 | Export Comic | Comic page layout | PDF / PNG file | User (External Entity) |
