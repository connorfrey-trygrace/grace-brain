# 2026-09-24 — Q&A Board: real typing indicator, bulk hide/unhide, emoji row removed

- **Typing indicator, now from AhaSlides' own socket:** the presenter page keeps a socket.io connection open in edit or present mode, and AhaSlides already subscribes it to `user-is-typing`. The board reaches that socket through the page's webpack runtime. It finds the connection-service module by its source containing `getSocket` and `setSocketId`, not by a hard-coded module id, and attaches a **listen-only** handler. Nothing is emitted.
  - Observed payload: `[participantId, true]`, sent when someone starts typing and repeated about every 16s while they continue. There is no stop event.
  - The board counts participants heard from in the last 17s and shows "Typing", or "N typing" when several people are. A question arriving clears the oldest typist.
  - If the hook fails (it retries up to 5 times), the board falls back to AhaSlides' present-mode bubble (`.chat-bubble.show`), and the panel header says "typing signal: present mode only".
  - Verified live on 2026-09-24 by typing into the audience question box in a second tab without submitting: the event fired and the board's hook counted 1 typist. The test box was cleared, and the joined count went up by one test participant.
- **Emoji palette removed** from the top-right stats. Floating reactions stay.
- **Panel filter + bulk hide:** the question list gets a **Hidden** filter chip, a category dropdown (with counts), an "N shown" count, and **Hide all** / **Unhide all** buttons that act on exactly what the current chip, category and search show. Bulk hide skips the question of the night. Hidden now means off the display everywhere: rotation, Top voted, Latest, and the category counts.
- **Also seen on the socket, for later:** `create-reaction` and `socket:online` / `socket:offline`, which could replace the 2s reaction and online-count polling.
