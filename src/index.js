// Minimal MCP-like stdio JSON-RPC server
// - Implements initialize, tools/list, tools/call
// - Adds resources/list and resources/read for built-in help
// - Provides community.* tools and auth.exchangeGoogleIdToken (stub verification)
//
// NOTE: This is a lightweight implementation that follows MCP conventions
// without using the official SDK. It uses Content-Length framed JSON-RPC over stdio.
// For production, consider using @modelcontextprotocol/sdk and robust token verification.

import crypto from 'node:crypto';
import { TextDecoder, TextEncoder } from 'node:util';

const enc = new TextEncoder();
const dec = new TextDecoder();

// -----------------------------
// JSON-RPC framing over stdio
// -----------------------------

/**
 * Send a JSON-RPC message framed with Content-Length
 */
function send(message) {
  const json = JSON.stringify(message);
  const body = enc.encode(json);
  const header = enc.encode(`Content-Length: ${body.byteLength}\r\n\r\n`);
  const out = new Uint8Array(header.byteLength + body.byteLength);
  out.set(header, 0);
  out.set(body, header.byteLength);
  process.stdout.write(out);
}

/**
 * Very small Content-Length parser for stdio streams.
 */
class StdioJsonRpc {
  constructor(onMessage) {
    this.buffer = Buffer.alloc(0);
    this.onMessage = onMessage;
    process.stdin.on('data', (chunk) => this._onData(chunk));
    process.stdin.on('end', () => process.exit(0));
  }

  _onData(chunk) {
    this.buffer = Buffer.concat([this.buffer, chunk]);
    while (true) {
      const headerEnd = this.buffer.indexOf('\r\n\r\n');
      if (headerEnd === -1) break;
      const headerBuf = this.buffer.subarray(0, headerEnd);
      const header = headerBuf.toString('utf8');
      const match = /Content-Length:\s*(\d+)/i.exec(header);
      if (!match) {
        // Drop garbage until next separator
        this.buffer = this.buffer.subarray(headerEnd + 4);
        continue;
      }
      const length = parseInt(match[1], 10);
      const messageStart = headerEnd + 4;
      if (this.buffer.byteLength < messageStart + length) break;
      const bodyBuf = this.buffer.subarray(messageStart, messageStart + length);
      const text = bodyBuf.toString('utf8');
      this.buffer = this.buffer.subarray(messageStart + length);
      try {
        const msg = JSON.parse(text);
        this.onMessage(msg);
      } catch (e) {
        // ignore malformed
      }
    }
  }
}

// -----------------------------
// In-memory data and helpers
// -----------------------------

const serverInfo = {
  name: 'OpenCommunity MCP Server',
  version: '0.1.0',
};

// Single-process connection context
const ctx = {
  sessionId: null,
  user: null, // { userId, email, name }
};

const rooms = new Map(); // roomId -> { id, name, visibility: 'public'|'private', createdAt }
const messages = []; // { id, roomId, userId, text, ts }

function nowIso() {
  return new Date().toISOString();
}

function makeId(prefix = '') {
  return prefix + crypto.randomBytes(6).toString('hex');
}

function requireAuth() {
  if (!ctx.user) {
    const err = new Error('Not authenticated. Call auth.exchangeGoogleIdToken first.');
    err.code = 'UNAUTHORIZED';
    throw err;
  }
}

// -----------------------------
// Tool registry and schemas
// -----------------------------

const tools = new Map();

function registerTool(def) {
  if (!def || !def.name || !def.inputSchema || !def.description || !def.handler) {
    throw new Error('Invalid tool definition');
  }
  tools.set(def.name, def);
}

function listToolsResponse() {
  return {
    tools: Array.from(tools.values()).map((t) => ({
      name: t.name,
      description: t.description,
      inputSchema: t.inputSchema,
    })),
  };
}

// Content helpers (MCP-style)
function textContent(text) {
  return { content: [{ type: 'text', text }] };
}

function jsonContent(obj) {
  return { content: [{ type: 'json', data: obj }] };
}

// -----------------------------
// Tools: help and auth
// -----------------------------

registerTool({
  name: 'help',
  description: 'Server quickstart and available categories.',
  inputSchema: { type: 'object', properties: {}, additionalProperties: false },
  handler: async () => textContent(
    [
      '# OpenCommunity MCP Server',
      '',
      'This server exposes auth.* and community.* tools.',
      '',
      'Auth flow:',
      '1) Obtain a Google ID token in your client (OAuth/OIDC).',
      '2) Call auth.exchangeGoogleIdToken with the ID token.',
      '3) Call community.* tools under your session.',
      '',
      'Tools overview:',
      '- auth.exchangeGoogleIdToken',
      '- community.listRooms, community.createRoom',
      '- community.postMessage, community.listMessages',
    ].join('\n')
  ),
});

registerTool({
  name: 'auth.exchangeGoogleIdToken',
  description: 'Exchange a Google ID token for a server session.',
  inputSchema: {
    type: 'object',
    additionalProperties: false,
    properties: {
      idToken: { type: 'string', description: 'Google ID token (JWT)' },
    },
    required: ['idToken'],
  },
  handler: async ({ idToken }) => {
    // WARNING: This is a stub that parses the JWT but does NOT verify
    // the signature. Replace with proper Google verification.
    const parts = (idToken || '').split('.');
    if (parts.length !== 3) {
      const err = new Error('Invalid JWT format');
      err.code = 'INVALID_ARGUMENT';
      throw err;
    }
    let payload;
    try {
      payload = JSON.parse(Buffer.from(parts[1], 'base64url').toString('utf8'));
    } catch {
      const err = new Error('Invalid JWT payload');
      err.code = 'INVALID_ARGUMENT';
      throw err;
    }
    const iss = payload.iss || '';
    if (!String(iss).includes('accounts.google.com')) {
      const err = new Error('Unexpected issuer; expected Google ID token');
      err.code = 'INVALID_ARGUMENT';
      throw err;
    }

    const userId = payload.sub || makeId('u_');
    const sessionId = makeId('s_');
    ctx.sessionId = sessionId;
    ctx.user = {
      userId,
      email: payload.email || null,
      name: payload.name || payload.email || 'User',
    };
    return jsonContent({
      sessionId,
      user: ctx.user,
      note: 'Token accepted (signature NOT verified in this demo).',
    });
  },
});

// -----------------------------
// Tools: community.*
// -----------------------------

registerTool({
  name: 'community.listRooms',
  description: 'List available rooms (public only).',
  inputSchema: {
    type: 'object',
    additionalProperties: false,
    properties: {},
  },
  handler: async () => {
    const data = Array.from(rooms.values())
      .filter((r) => r.visibility === 'public')
      .map((r) => ({ id: r.id, name: r.name, visibility: r.visibility, createdAt: r.createdAt }));
    return jsonContent({ rooms: data });
  },
});

registerTool({
  name: 'community.createRoom',
  description: 'Create a new room (requires auth).',
  inputSchema: {
    type: 'object',
    additionalProperties: false,
    properties: {
      name: { type: 'string', minLength: 1 },
      visibility: { type: 'string', enum: ['public', 'private'], default: 'public' },
    },
    required: ['name'],
  },
  handler: async ({ name, visibility = 'public' }) => {
    requireAuth();
    const id = makeId('r_');
    const room = { id, name: String(name).slice(0, 80), visibility, createdAt: nowIso() };
    rooms.set(id, room);
    return jsonContent({ room });
  },
});

registerTool({
  name: 'community.postMessage',
  description: 'Post a message to a room (requires auth).',
  inputSchema: {
    type: 'object',
    additionalProperties: false,
    properties: {
      roomId: { type: 'string' },
      text: { type: 'string', minLength: 1, maxLength: 2000 },
    },
    required: ['roomId', 'text'],
  },
  handler: async ({ roomId, text }) => {
    requireAuth();
    if (!rooms.has(roomId)) {
      const err = new Error('Room not found');
      err.code = 'NOT_FOUND';
      throw err;
    }
    const id = makeId('m_');
    const msg = { id, roomId, userId: ctx.user.userId, text: String(text), ts: Date.now() };
    messages.push(msg);
    return jsonContent({ message: msg });
  },
});

registerTool({
  name: 'community.listMessages',
  description: 'List recent messages for a room.',
  inputSchema: {
    type: 'object',
    additionalProperties: false,
    properties: {
      roomId: { type: 'string' },
      limit: { type: 'number', minimum: 1, maximum: 200, default: 50 },
      afterTs: { type: 'number', description: 'Only messages with ts > afterTs' },
    },
    required: ['roomId'],
  },
  handler: async ({ roomId, limit = 50, afterTs }) => {
    if (!rooms.has(roomId)) {
      const err = new Error('Room not found');
      err.code = 'NOT_FOUND';
      throw err;
    }
    let list = messages.filter((m) => m.roomId === roomId);
    if (typeof afterTs === 'number') {
      list = list.filter((m) => m.ts > afterTs);
    }
    list = list.sort((a, b) => a.ts - b.ts).slice(-limit);
    return jsonContent({ messages: list });
  },
});

// -----------------------------
// Resources: help
// -----------------------------

const resources = new Map();
resources.set('resource://help/quickstart', {
  uri: 'resource://help/quickstart',
  mimeType: 'text/markdown',
  text: [
    '# Quickstart',
    '',
    '1) Initialize and list tools.',
    '2) Obtain Google ID token in your client.',
    '3) Call auth.exchangeGoogleIdToken with the token.',
    '4) Use community.* tools.',
  ].join('\n'),
});

// -----------------------------
// JSON-RPC method handlers
// -----------------------------

function reply(id, result) {
  send({ jsonrpc: '2.0', id, result });
}

function error(id, code, message, data) {
  send({ jsonrpc: '2.0', id, error: { code, message, data } });
}

function onMessage(msg) {
  const { id, method, params } = msg;
  if (method === 'initialize') {
    return reply(id, {
      protocolVersion: '2024-11-05',
      serverInfo,
      capabilities: {
        tools: {},
        resources: {},
      },
    });
  }
  if (method === 'tools/list') {
    return reply(id, listToolsResponse());
  }
  if (method === 'tools/call') {
    const name = params?.name;
    const args = params?.arguments || {};
    const tool = tools.get(name);
    if (!tool) return error(id, -32601, `Tool not found: ${name}`);
    Promise.resolve()
      .then(() => tool.handler(args))
      .then((res) => reply(id, res))
      .catch((e) => {
        const code = e?.code === 'UNAUTHORIZED' ? 401
          : e?.code === 'NOT_FOUND' ? 404
          : e?.code === 'INVALID_ARGUMENT' ? 400
          : -32000;
        error(id, code, e?.message || 'Tool error');
      });
    return;
  }
  if (method === 'resources/list') {
    const list = Array.from(resources.values()).map((r) => ({ uri: r.uri, mimeType: r.mimeType }));
    return reply(id, { resources: list });
  }
  if (method === 'resources/read') {
    const uri = params?.uri;
    const r = resources.get(uri);
    if (!r) return error(id, 404, `Resource not found: ${uri}`);
    return reply(id, {
      contents: [
        {
          uri: r.uri,
          mimeType: r.mimeType,
          text: r.text,
        },
      ],
    });
  }
  // Graceful shutdown
  if (method === 'shutdown') {
    reply(id, null);
    return;
  }
  if (method === 'exit') {
    process.exit(0);
  }
  return error(id, -32601, `Method not found: ${method}`);
}

// Start server
process.stdin.resume();
new StdioJsonRpc(onMessage);

