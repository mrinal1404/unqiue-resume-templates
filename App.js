import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [formData, setFormData] = useState({
    name: '',
    experience: '',
    skills: '',
    education: '',
    projects: '',
    objective: '',
  });
  const [resumeContent, setResumeContent] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5001/generate-resume', formData);
      setResumeContent(response.data.resume);
    } catch (error) {
      console.error('Error generating resume:', error);
    }
  };

  return (
    <div className="App">
      <h1>AI Resume Generator</h1>
      <form onSubmit={handleSubmit}>
        <input name="name" placeholder="Name" value={formData.name} onChange={handleChange} />
        <input name="experience" placeholder="Experience" value={formData.experience} onChange={handleChange} />
        <input name="skills" placeholder="Skills" value={formData.skills} onChange={handleChange} />
        <input name="education" placeholder="Education" value={formData.education} onChange={handleChange} />
        <input name="projects" placeholder="Projects" value={formData.projects} onChange={handleChange} />
        <input name="objective" placeholder="Objective" value={formData.objective} onChange={handleChange} />
        <button type="submit">Generate Resume</button>
      </form>
      
      {/* Render the HTML directly */}
      {resumeContent && (
        <div>
          <h2>Generated Resume:</h2>
          <div dangerouslySetInnerHTML={{ __html: resumeContent }} />
        </div>
      )}
    </div>
  );
}

export default App;
