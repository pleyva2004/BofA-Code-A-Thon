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

  return (
    <div className="sidebar">
      <div>
        <h2 className="sidebar-title">Courses</h2>
        <div className="tag-container">
          {courses.map((course, index) => (
            <CourseBubble key={index} text={course} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default CourseSidebar;