# How the Email Drafts Kanban was built (2026-11-20)

Record of the exact steps. Do not edit; add a new dated file for changes.

## Tools that made it possible
1. **Attio REST API v2** (`ATTIO_API_KEY`, base `https://api.attio.com/v2`): create a `status`-type attribute and its statuses on a custom object.
2. **Attio MCP connector tool `create-view`**: creates a saved view of `type: "kanban"` with `kanban.status_attribute`. This is the step that creates the Kanban board. Its sibling tools are `list-views`, `get-view`, `update-view` and `delete-view`.
   - Unknown: when Attio added `create-view` to the MCP connector. It was available in this session (2026-11-20).

## Requirement found
A Kanban groups by a **status-type** attribute. A `select` attribute does not work. The old `email_drafts.status` was `select`, so a new attribute was needed.

## Steps (exact)
1. Create the attribute (REST):
   `POST /objects/email_drafts/attributes`
   ```json
   {"data": {"title": "Stage", "api_slug": "stage", "type": "status",
             "description": "Draft lifecycle. Drag in the Kanban to change. ...",
             "is_required": false, "is_unique": false, "is_multiselect": false, "config": {}}}
   ```
2. Add the statuses (REST), one call each, in column order:
   `POST /objects/email_drafts/attributes/stage/statuses` with `{"data": {"title": "<T>"}}`
   for T = Drafted, Reviewed, Approved, Pushed, Failed, Superseded.
   (The new attribute had no default statuses. If it has defaults, archive them with
   `PATCH /objects/email_drafts/attributes/stage/statuses/{status_id}` `{"data": {"is_archived": true}}`.)
3. Copy values (REST): for each record, `PATCH /objects/email_drafts/records/{id}` with
   `{"data": {"values": {"stage": "<old status title>"}}}`. Result: 44 of 44 copied, 0 mismatches.
4. Archive the old field (REST): `PATCH /objects/email_drafts/attributes/status`
   `{"data": {"title": "Status (old, use Stage)", "is_archived": true}}`.
5. Create the Kanban view (Attio MCP tool `create-view`):
   ```json
   {"object": "email_drafts", "title": "Email Drafts – Kanban", "type": "kanban",
    "kanban": {"status_attribute": "stage", "show_no_status_column": false},
    "filter": {"attribute": "stage", "op": "not_eq", "value": "Superseded"},
    "attributes": [{"attribute": "name"}, {"attribute": "kind"}, {"attribute": "subject"},
                   {"attribute": "review_notes"}, {"attribute": "push_result"}, {"attribute": "drafted_at"}],
    "sorts": [{"attribute": "drafted_at", "direction": "desc"}]}
   ```
   Result: `view_id f1312ab6-bb19-47e6-be1d-524a31d08c21`.
6. Point the scripts at `stage` (read, write, query filter `{"stage": "Approved"}`). See commit 147ff33.

## Behavior
- Dragging a card between columns changes `stage` on the record.
- The push skill reads `stage = Approved`, so a drag to Approved is an approval.
- Do not drag to Pushed by hand: only the push skill can confirm that a draft is in Outreach.

## Reuse on another object
Repeat steps 1–2 (a status-type attribute), then step 5 with that object and attribute slug.
