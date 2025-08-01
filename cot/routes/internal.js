const express = require('express');
const router = express.Router();

// Only users with is_internal=true can see the flag
router.get('/internal/flag', (req, res) => {
  if (!req.session.is_internal) return res.status(403).send('Not internal');
  return res.send(`Flag: ${process.env.FLAG}`);
});

module.exports = router;

