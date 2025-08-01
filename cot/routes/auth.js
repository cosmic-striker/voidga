const express = require('express');
const axios = require('axios');
const { injectCsrf, validateCsrf } = require('../middleware/csrf');
const router = express.Router();

// Show link button
router.get('/login', injectCsrf, (req, res) => {
  res.render('login');
});

// Kick off OAuth: one-click “Link with Google”
router.post('/link/google', (req, res) => {
  const { csrf } = req.body;
  if (!validateCsrf(csrf)) return res.status(403).send('CSRF failure');
  const params = new URLSearchParams({
    client_id: process.env.OAUTH_CLIENT_ID,
    redirect_uri: 'http://localhost:3000/auth/google/callback',
    state: csrf,
    scope: 'profile offline_access'
  });
  return res.redirect(`http://localhost:3000/oauth/authorize?${params}`);
});

// OAuth callback
router.get('/auth/google/callback', async (req, res) => {
  const { code, state } = req.query;
  if (!validateCsrf(state)) return res.status(403).send('Bad CSRF state');
  // Exchange code for tokens
  const resp = await axios.post('http://localhost:3000/oauth/token', new URLSearchParams({
    grant_type: 'authorization_code',
    code, client_id: process.env.OAUTH_CLIENT_ID,
    client_secret: process.env.OAUTH_CLIENT_SECRET
  }), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } });
  // Save tokens in session
  req.session.tokens = { access: resp.data.access_token, refresh: resp.data.refresh_token };
  return res.redirect('/dashboard');
});

module.exports = router;

