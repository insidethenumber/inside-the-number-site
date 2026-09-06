# Why a newsletter ships with no graphics — and the only method that works

**Found Sep 6, 2026.** Chuck: "No graphics, nothing but text. Why? I thought we had this figured out."

## The rule

beehiiv's email renderer renders **only** `imageBlock` nodes whose file lives on
beehiiv's own CDN (`isUploaded: true`, src on
`beehiiv-images-production.s3.amazonaws.com`).

Anything else is **accepted by the editor, looks correct on screen, and is then
silently dropped** from both the email and the web post. No error, no warning,
no broken-image icon. Just gone.

Three things that all LOOK fine in the editor and all ship as text:

| What you put in the doc | Editor | Email |
|---|---|---|
| `<img src="https://insidethenumber.com/...">` | renders | **dropped** |
| `<figure data-type="imageBlock" data-src="https://insidethenumber.com/..." data-is-uploaded="false">` | renders | **dropped** |
| `<figure data-type="imageBlock" data-src="https://beehiiv-images-production.s3.../..." data-is-uploaded="true">` | renders | **ships** |

The editor renders the first two because a browser will display any `<img>`
inside a contenteditable. That is why this passes a visual check and still
fails. **A visual check of the editor is not a verification.**

## Verification that actually catches it

Never trust the editor. After building the body, run:

    get_post_content(post_id, format="html")

and confirm the image count in that HTML is what you expect. That is the real
email render. If the images are missing there, they will be missing in the
inbox. `format="text"` will not tell you anything — it strips images by design.

## How to get bytes into beehiiv's media library

The MCP write tools (`save_image`, `save_post`, `edit_post_content`,
`duplicate_post`, `edit_post`) are **all gated on the Launch plan** and return
"not available on your current plan". The Chrome `file_upload` tool is also
unavailable in this session type. So neither obvious path works.

The method that does work, from a browser session on app.beehiiv.com:

1. The images are already published to `insidethenumber.com/assets/newsletter/<date>/`
   by `scripts/newsletter_assets.py`.
2. `_headers` sets `Access-Control-Allow-Origin: *` on `/assets/newsletter/*`
   (added Sep 6, 2026 for exactly this), so the beehiiv tab can fetch them.
3. In the beehiiv editor tab:

   ```js
   const r = await fetch('https://insidethenumber.com/assets/newsletter/<date>/header.jpg');
   const file = new File([await r.blob()], 'header.jpg', {type:'image/jpeg'});
   const inp = document.querySelector('input[type=file]');
   const dt = new DataTransfer(); dt.items.add(file);
   Object.defineProperty(inp, 'files', {value: dt.files, configurable: true});
   inp.dispatchEvent(new Event('change', {bubbles: true}));
   ```
   Wait ~6s per image. beehiiv uploads it to its own CDN.
4. `list_assets(publication_id)` returns the new asset IDs (newest first).
5. Build the body with real `imageBlock` figures pointing at
   `https://beehiiv-images-production.s3.amazonaws.com/uploads/asset/file/<asset-id>/<filename>?t=<ts>`
   and `data-is-uploaded="true"`, then
   `document.querySelector('.tiptap.ProseMirror').editor.commands.setContent(HTML, true)`.
6. Re-verify with `get_post_content(format="html")` before scheduling.

## What actually broke on Sep 6 — and why the automation is FINE

The scheduled newsletter tasks were never broken. **I broke this issue by
taking a shortcut the task prompts do not use.**

The documented method (itn-daily-weekday / itn-daily-weekend, STEP 4b) pastes
the body as a real `ClipboardEvent` carrying `text/html`. beehiiv's editor has
a **paste handler that ingests external `<img>` URLs and uploads them to its own
CDN**. That is why every issue built by the tasks has beehiiv-hosted images.

I used `editor.commands.setContent(HTML, true)` instead, because it is cleaner
and avoids the leftover-paragraph quirk. `setContent` writes straight to the
document and **never fires the paste handler**, so the external URLs were stored
verbatim, rendered fine on screen, and were dropped at send.

### The rule that follows

**Never build a newsletter body with `setContent`.** Use the ClipboardEvent
paste in STEP 4b, or upload the images first (above) and reference
beehiiv-hosted URLs. `setContent` is safe only when every `imageBlock` in the
HTML already points at `beehiiv-images-production.s3.amazonaws.com` with
`data-is-uploaded="true"`.
