const express = require('express');
const { PythonShell } = require('python-shell');
const path = require('path');  // Import the 'path' module
const app = express();
const port = 3000;

// Define a route to run the Python script
app.get('/run-python-script', (req, res) => {
  // Specify the path to your Python script
  const pythonScriptPath = path.join(__dirname, 'api.py');

  // Options for the Python script execution
  const options = {
    scriptPath: __dirname,  // Specify the directory containing api.py
    args: [/* Pass any command-line arguments if needed */],
  };

  // Run the Python script
  PythonShell.run(pythonScriptPath, options, (err, results) => {
    if (err) {
      console.error('Error during Python script execution:', err);
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      // Process results from the Python script
      console.log('Python script executed successfully:', results);
      res.json({ result: results });
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
