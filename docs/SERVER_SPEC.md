MCP Server Contract: OpenCommunity
==================================

Overview
- Transport: Content-Length framed JSON-RPC over stdio.
- Methods: `initialize`, `tools/list`, `tools/call`, `resources/list`, `resources/read`.
- Server info: name `OpenCommunity MCP Server`, version `0.1.0`.

Initialize
- Request:
```
{ "jsonrpc":"2.0", "id":1, "method":"initialize", "params":{} }
```
- Response:
```
{
  "jsonrpc":"2.0",
  "id":1,
  "result": {
    "protocolVersion":"2024-11-05",
    "serverInfo": {"name":"OpenCommunity MCP Server","version":"0.1.0"},
    "capabilities": {"tools":{},"resources":{}}
  }
}
```

Tools Discovery
- Request: `{ "jsonrpc":"2.0", "id":2, "method":"tools/list" }`
- Response: `{ "jsonrpc":"2.0","id":2, "result": { "tools": [ ... ] } }`

Tool: help
- Name: `help`
- Description: Server quickstart and categories.
- InputSchema: `{ "type":"object", "properties":{}, "additionalProperties":false }`
- `tools/call` Example:
```
{ "jsonrpc":"2.0", "id":3, "method":"tools/call",
  "params":{ "name":"help", "arguments":{} } }
```
- Result: `{ "content": [{"type":"text","text":"..."}] }`

Tool: auth.exchangeGoogleIdToken
- Name: `auth.exchangeGoogleIdToken`
- Description: Exchange Google ID token for a server session (demo: no signature verification).
- InputSchema:
```
{
  "type":"object", "additionalProperties":false,
  "properties":{ "idToken": {"type":"string","description":"Google ID token (JWT)"} },
  "required":["idToken"]
}
```
- Result Content: `{ "content": [{"type":"json", "data": { "sessionId":"s_...", "user":{...} } }] }`

Tool: community.listRooms
- Name: `community.listRooms`
- Description: List public rooms.
- InputSchema: `{ "type":"object", "properties":{}, "additionalProperties":false }`
- Result: `{ "content": [{"type":"json","data": { "rooms":[{id,name,visibility,createdAt}] }}] }`

Tool: community.createRoom
- Name: `community.createRoom`
- Description: Create new room. Requires authenticated session.
- InputSchema:
```
{
  "type":"object", "additionalProperties":false,
  "properties":{
    "name":{"type":"string","minLength":1},
    "visibility":{"type":"string","enum":["public","private"],"default":"public"}
  },
  "required":["name"]
}
```
- Result: `{ "content":[{"type":"json","data": { "room": {id,name,visibility,createdAt} }}] }`

Tool: community.postMessage
- Name: `community.postMessage`
- Description: Post a message to a room. Requires authenticated session.
- InputSchema:
```
{
  "type":"object","additionalProperties":false,
  "properties":{ "roomId":{"type":"string"}, "text":{"type":"string","minLength":1,"maxLength":2000} },
  "required":["roomId","text"]
}
```
- Result: `{ "content":[{"type":"json","data": { "message": {id,roomId,userId,text,ts} }}] }`

Tool: community.listMessages
- Name: `community.listMessages`
- Description: List recent messages in a room.
- InputSchema:
```
{
  "type":"object","additionalProperties":false,
  "properties":{ "roomId":{"type":"string"}, "limit":{"type":"number","minimum":1,"maximum":200,"default":50}, "afterTs":{"type":"number"} },
  "required":["roomId"]
}
```
- Result: `{ "content":[{"type":"json","data": { "messages": [{id,roomId,userId,text,ts}] }}] }`

Resources
- `resources/list` → `{ resources: [{ uri, mimeType }] }`
- `resources/read` with `{ uri }` → `{ contents: [{ uri, mimeType, text }] }`
- Provided: `resource://help/quickstart` (text/markdown)

Errors
- JSON-RPC error codes used:
  - 400: INVALID_ARGUMENT
  - 401: UNAUTHORIZED
  - 404: NOT_FOUND
  - -32000: generic tool error

Auth Notes (production)
- Verify Google ID token signature using Google JWKS (`kid` from header), issuer, audience, exp.
- Associate session to connection; avoid sending tokens on every call.
- Consider per-room ACLs, moderation tools, and rate limiting.

