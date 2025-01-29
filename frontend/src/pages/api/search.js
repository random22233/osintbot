import { exec } from 'child_process';

// Proxy API to handle the search request
export default function handler(req, res) {
  const { query } = req.query;

  if (!query) {
    return res.status(400).json({ error: 'Query parameter is required' });
  }

  // Run the appropriate Python script (email.py or username.py) based on the query
  let command = '';
  if (query.includes('@')) { // If it's an email
    command = `python email.py ${query} ${process.env.REVERSE_CONTACT_API_KEY}`;
  } else { // If it's a username
    command = `python username.py ${query} ${process.env.PEOPLE_DATA_LABS_API_KEY}`;
  }

  exec(command, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({ error: `Error executing Python script: ${stderr || error.message}` });
    }

    try {
      // Parse the output (assumed to be in JSON format)
      const data = JSON.parse(stdout);

      if (!data) {
        return res.status(404).json({ error: 'No data found for the query' });
      }

      // Send the data to the frontend
      res.status(200).json(data);
    } catch (err) {
      return res.status(500).json({ error: 'Error parsing Python script output' });
    }
  });
}
