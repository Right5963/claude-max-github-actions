module.exports = {
  apps: [{
    name: 'claude-mcp-runner',
    cwd: './actions-runner',
    script: './run.sh',
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    }
  }, {
    name: 'perplexity-mcp-server',
    script: './perplexity_mcp_server.py',
    args: 'mcp-server',
    interpreter: 'python3',
    autorestart: true,
    watch: false,
    max_memory_restart: '500M'
  }]
};
