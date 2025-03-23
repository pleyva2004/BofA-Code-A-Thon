// UniversitySelector.tsx
import React, { useState, useEffect } from 'react';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

console.log('Supabase URL:', supabaseUrl);
console.log('Supabase Key exists:', !!supabaseKey);

const supabase = createClient(supabaseUrl!, supabaseKey!);

interface UniversitySelectorProps {
  selectedUniversity: string;
  setSelectedUniversity: (value: string) => void;
  // Optional: callback when a new university is added
  onAddUniversity?: (newUniversity: string) => void;
}

const UniversitySelector: React.FC<UniversitySelectorProps> = ({ selectedUniversity, setSelectedUniversity, onAddUniversity }) => {
  console.log('UniversitySelector component mounted');
  
  const predefinedUniversities = [
    "New Jersey Institute of Technology",
    "Rutgers New Brunswick",
    "University of Texas, Arlington",
    "North Carolina A&T University",
    "Kennesaw State University",
    "Howard University",
    "Tennessee State University",
    "Johnson C. Smith University",
    "University of North Carolina, Charlotte"
  ];
  
  const [newUniversity, setNewUniversity] = React.useState('');
  const [message, setMessage] = React.useState('');

  const handleAddUniversity = async () => {
    if (newUniversity.trim() === '') {
      setMessage("Please enter a university name.");
      return;
    }
    // Insert into your Supabase table (this example assumes you're doing that)
    const { data, error } = await supabase
      .from('university_courses')
      .insert([{ university_name: newUniversity, matched_courses: {} }]);

    if (error) {
      console.error("Error adding university:", error);
      setMessage("Error adding university.");
    } else {
      console.log("Added university:", data);
      setMessage("University added successfully!");
      // Optionally update the selected university
      setSelectedUniversity(newUniversity);
      // And/or call a provided callback
      if (onAddUniversity) {
        onAddUniversity(newUniversity);
      }
      setNewUniversity('');
    }
  };

  const initializeUniversities = async () => {
    console.log('Starting university initialization');
    
    for (const university of predefinedUniversities) {
      console.log(`Processing ${university}`);
      
      try {
        // Check if university exists
        const { data: existingUniversity, error: checkError } = await supabase
          .from('university_courses')
          .select('university_name')
          .eq('university_name', university)
          .single();

        if (checkError) {
          console.error(`Error checking ${university}:`, checkError);
          continue;
        }

        if (!existingUniversity) {
          const { data, error } = await supabase
            .from('university_courses')
            .insert([{ 
              university_name: university, 
              matched_courses: {} 
            }])
            .select();

          if (error) {
            console.error(`Error adding ${university}:`, error);
          } else {
            console.log(`Successfully added ${university}`);
          }
        } else {
          console.log(`${university} already exists`);
        }
      } catch (error) {
        console.error(`Unexpected error processing ${university}:`, error);
      }
    }
  };

  useEffect(() => {
    console.log('Running initialization effect');
    initializeUniversities();
  }, []);

  return (
    <div className="flex justify-center items-center p-5">
      <div className="flex flex-col md:flex-row items-center gap-4">
        <label 
          htmlFor="university-dropdown" 
          className="text-2xl font-extrabold text-indigo-600 uppercase tracking-wider"
        >
          Select a university:
        </label>
        
        <select
          id="university-dropdown"
          value={selectedUniversity}
          onChange={(e) => setSelectedUniversity(e.target.value)}
          className="rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2"
        >
          {predefinedUniversities.map((uni, index) => (
            <option key={index} value={uni}>{uni}</option>
          ))}
        </select>

        <span className="text-gray-600 font-medium">or add your university:</span>

        <input
          type="text"
          placeholder="Enter university name"
          value={newUniversity}
          onChange={(e) => setNewUniversity(e.target.value)}
          className="rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-4 py-2"
        />

        <button 
          onClick={handleAddUniversity}
          className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
        >
          Add University
        </button>

        {message && (
          <p className={`text-sm ${message.includes('Error') ? 'text-red-600' : 'text-green-600'}`}>
            {message}
          </p>
        )}
      </div>
    </div>
  );
};

export default UniversitySelector;
