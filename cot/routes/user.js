const express = require('express');
const { injectCsrf, validateCsrf } = require('../middleware/csrf');
const router = express.Router();

router.get('/dashboard', injectCsrf, (req, res) => {
  const linked = !!(req.session.tokens || {}).access;
  res.render('dashboard', { linked });
});

// Toggle internal flag (vulnerable CSRF)
router.post('/user/settings', (req, res) => {
  const { csrf, internal } = req.body;
  if (!validateCsrf(csrf)) return res.status(403).send('CSRF failure');
  req.session.is_internal = internal === 'on';
  res.redirect('/dashboard');
});

module.exports = router;

