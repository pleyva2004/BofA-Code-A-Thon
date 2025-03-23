// CourseDataFetcher.tsx
import React, { useState } from 'react';

interface CourseDataFetcherProps {
  universityName: string;
  career: string;
}

const CourseDataFetcher: React.FC<CourseDataFetcherProps> = ({ universityName, career }) => {
  const [courseData, setCourseData] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFetchCourses = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('/api/fetch-courses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ universityName, career })
      });
      const result = await response.json();
      if (response.ok) {
        setCourseData(result.matchedCourses);
      } else {
        setError(result.error || 'Failed to fetch course data.');
      }
    } catch (err: any) {
      setError(err.message || 'Unexpected error.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <button 
        onClick={handleFetchCourses} 
        className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors"
      >
        Fetch Courses for {universityName}
      </button>
      {loading && <p>Loading course data...</p>}
      {error && <p className="text-red-600">{error}</p>}
      {courseData && (
        <div className="mt-4">
          <h3 className="font-bold text-xl">Matched Courses:</h3>
          <pre className="bg-gray-100 p-4 rounded">{courseData}</pre>
        </div>
      )}
    </div>
  );
};

export default CourseDataFetcher;
