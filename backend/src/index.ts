import express from 'express';
import cors from 'cors';
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';

dotenv.config();

// Server configuration
const app = express();
app.use(cors());
app.use(express.json());

// Initialize Supabase client
const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_ANON_KEY!;
const supabase = createClient(supabaseUrl, supabaseKey);

// Endpoint to get all jobs
app.get('/api/jobs', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('jobs')
      .select('*');
    
    if (error) throw error;
    
    res.json(data);
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
});

// Endpoint to get resource categories for a specific job
app.get('/api/jobs/:id/resources', async (req, res) => {
  const jobId = req.params.id;
  try {
    const { data, error } = await supabase
      .from('job_resource_categories')
      .select('*')
      .eq('job_id', jobId);
    
    if (error) throw error;
    
    res.json(data);
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});


/* 
SQL EDITOR CODE FOR SUPABASE
```
CREATE TABLE IF NOT EXISTS jobs (
  id serial PRIMARY KEY,
  job_title text NOT NULL DEFAULT 'string',
  overview text NOT NULL DEFAULT 'string'
);

CREATE TABLE IF NOT EXISTS job_resource_categories (
  id serial PRIMARY KEY,
  job_id integer NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
  category_name text NOT NULL DEFAULT 'string',
  resources jsonb NOT NULL DEFAULT '[]'
);
```
*/