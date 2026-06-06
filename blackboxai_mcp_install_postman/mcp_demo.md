# Postman MCP Server demo

## 1) Configure the API key

The local Postman MCP server requires `POSTMAN_API_KEY`.

Set it in your shell:

```bash
export POSTMAN_API_KEY="<YOUR_POSTMAN_API_KEY>"
```

## 2) Verify the server starts

From this folder:

```bash
cd /Users/andy/blackboxai_mcp_install_postman
npx -y @postman/postman-mcp-server --minimal
```

You should see MCP/stdio logs.

## 3) Demonstrate a tool capability

A simple first capability to test is listing workspaces (tool name depends on the MCP version: in v2.x it is typically `getWorkspaces`).

Run with an MCP client/host. If you have an MCP host available, add the server from `blackbox_mcp_settings.json` and then invoke:

- `getWorkspaces`

Expected result: JSON listing available Postman workspaces you have access to.

## 4) One-shot demo with `npx` (if your environment supports it)

If your MCP host supports ad-hoc invocation, send a request such as:

> Call `getWorkspaces`.

and capture the tool output.
