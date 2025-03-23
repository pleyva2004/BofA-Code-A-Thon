import React from 'react';

interface CourseBubbleProps {
  text: string;
}

const CourseBubble: React.FC<CourseBubbleProps> = ({ text }) => {
  return (
    <div className="tag">{text}</div>
  );
};

const CourseSidebar: React.FC = () => {
  const courses = [
    'CS101: Introduction to Computer Science',
    'CS201: Data Structures & Algorithms',
    'CS301: Operating Systems',
    'CS315: Databases & Information Systems',
    'CS420: Machine Learning Fundamentals',
    'CS499: Capstone Project'
  ];
  
  /* EDIT THIS IN THE FUTURE TO FORMAT CLASS DATA BETTER*/
  return (
    <div className="sidebar p-4 bg-white rounded-xl shadow-md w-64">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-gray-800 mb-2">Your Universities Courses</h2>
        <div className="flex flex-wrap gap-2">
          {courses.map((course, index) => (
            <CourseBubble key={index} text={course} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default CourseSidebar;