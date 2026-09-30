**Team ID:** SWTID-2026-9211  
**Project Title:** ComicCraft - AI Comic Story Creator using Gemini Models  
**Team Size:** 5  
**Team Leader:** Dharshini  
**Team Members:** Pavi, J. Sakthi Devathai, Pavithra Mahadevan, Bhuvaneshwari

---

# Functional and Performance Testing

## Functional Test Cases

| Test Case ID | Module | Test Scenario | Test Steps | Expected Result | Actual Result | Status | Tested By |
|--------------|--------|---------------|------------|-----------------|---------------|--------|-----------|
| TC-01 | Story Input | Submit valid story idea | Enter idea, choose style, 4 panels, click Generate | Request accepted | Request accepted | Pass | Bhuvaneshwari |
| TC-02 | Story Input | Submit empty story | Leave idea blank and click Generate | Validation message shown | Validation message shown | Pass | Bhuvaneshwari |
| TC-03 | Script Generation | Generate script for 4 panels | Submit valid idea | JSON with 4 panels returned | 4 panels returned | Pass | Pavi |
| TC-04 | Script Generation | Handle invalid JSON | Simulate malformed model output | Retry and parse successfully | Parsed after retry | Pass | Pavi |
| TC-05 | Character Sheet | Character consistency | Generate 4 panels with same hero | Same hero appearance in all panels | Mostly consistent | Pass | Pavithra Mahadevan |
| TC-06 | Image Generation | Generate panel image | Send scene prompt | Image returned | Image returned | Pass | J. Sakthi Devathai |
| TC-07 | Art Style | Change style to Manga | Select Manga and generate | Panels in manga style | Manga style applied | Pass | Pavithra Mahadevan |
| TC-08 | Speech Bubble | Dialogue overlay | Generate panel with dialogue | Text readable inside bubble | Readable | Pass | Bhuvaneshwari |
| TC-09 | Edit & Regenerate | Regenerate one panel | Click regenerate on panel 2 | Only panel 2 updated | Only panel 2 updated | Pass | J. Sakthi Devathai |
| TC-10 | Export | Download PDF | Click Download PDF | PDF with all panels opens | PDF opened correctly | Pass | Dharshini |
| TC-11 | Safety | Unsafe story input | Enter harmful content | Request blocked with message | Blocked | Pass | Dharshini |
| TC-12 | Error Handling | Invalid API key | Use wrong key | Friendly error message | Error message shown | Pass | Dharshini |

## Performance Testing

| S.No | Parameter | Test Condition | Target | Result | Status |
|------|-----------|----------------|--------|--------|--------|
| 1 | Script generation time | 4-panel story | Under 10 sec | About 6 sec | Pass |
| 2 | Single panel image time | 1 panel | Under 30 sec | About 18 sec | Pass |
| 3 | Full comic time | 4 panels | Under 2 min | About 80 sec | Pass |
| 4 | Export time | PDF of 4 panels | Under 5 sec | About 2 sec | Pass |
| 5 | App load time | Home page | Under 3 sec | About 2 sec | Pass |
| 6 | Error rate | 20 test runs | Below 10% | 5% | Pass |
