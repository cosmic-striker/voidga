const crypto = require('crypto');
const TOKENS = {};    // store codes → user
const CLIENTS = {
  [process.env.OAUTH_CLIENT_ID]: process.env.OAUTH_CLIENT_SECRET
};

// 1) Authorize endpoint: auto-approve, redirect back with code
async function authorize(req, res) {
  const { client_id, redirect_uri, state, scope } = req.query;
  if (!CLIENTS[client_id]) return res.status(400).send('Unknown client');
  // grant a one-time code
  const code = crypto.randomBytes(8).toString('hex');
  TOKENS[code] = { scope, issued: Date.now() };
  // silent consent even for offline_access
  return res.redirect(`${redirect_uri}?code=${code}&state=${state}`);
}

// 2) Token endpoint: exchange code for tokens
async function token(req, res) {
  const { grant_type, code, client_id, client_secret } = req.body;
  if (grant_type !== 'authorization_code') return res.status(400).send('Bad grant');
  if (CLIENTS[client_id] !== client_secret) return res.status(401).send('Forbidden');
  const info = TOKENS[code];
  if (!info) return res.status(400).send('Invalid code');
  // Issue access token (short) + refresh token if offline_access
  const at = crypto.randomBytes(16).toString('hex');
  const rt = info.scope.includes('offline_access')
    ? crypto.randomBytes(24).toString('hex')
    : null;
  return res.json({ access_token: at, refresh_token: rt, token_type: 'Bearer', expires_in: 3600 });
}

module.exports = { authorize, token };

