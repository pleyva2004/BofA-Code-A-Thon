import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import './MindMap.css';

interface Node {
  id: string;
  name: string;
  type: 'main' | 'category' | 'subcategory';
  children?: Node[];
  description?: string;
}

interface HierarchyNodeWithCoords extends d3.HierarchyNode<Node> {
  x: number;
  y: number;
}

interface PopupProps {
  node: Node;
  position: { x: number; y: number };
  onClose: () => void;
}

const Popup: React.FC<PopupProps> = ({ node, position, onClose }) => {
  const popupRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (popupRef.current && !popupRef.current.contains(event.target as Element)) {
        onClose();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [onClose]);

  return (
    <div 
      className="mind-map-popup" 
      style={{ 
        left: position.x, 
        top: position.y 
      }}
      ref={popupRef}
    >
      <div className="popup-header">
        <h3>{node.name}</h3>
        <button className="close-button" onClick={onClose}>×</button>
      </div>
      <div className="popup-content">
        <p>{node.description || "No description available for this item yet."}</p>
      </div>
    </div>
  );
};

const MindMapGD: React.FC = () => {
  const svgRef = useRef<SVGSVGElement>(null);
  const gRef = useRef<SVGGElement | null>(null);
  const [popup, setPopup] = useState<{ node: Node; position: { x: number; y: number } } | null>(null);

  const renderMindMap = () => {
    if (!svgRef.current) return;

    // Clear any existing SVG content
    d3.select(svgRef.current).selectAll("*").remove();

    // Mind map data structure with descriptions
    const data: Node = {
      id: "root",
      name: "Game Development (edit hardcoded data later)",
      type: "main",
      description: "A frontend developer creates the user interface and user experience of websites and applications. They work with HTML, CSS, and JavaScript to build responsive and interactive web pages.",
      children: [
        {
          id: "skills",
          name: "Skills",
          type: "category",
          description: "Core skills needed for frontend development include HTML, CSS, JavaScript, and frameworks like React, Angular, or Vue. Knowledge of responsive design and accessibility is also important.",
          children: [
            { 
              id: "youtubers", 
              name: "Youtubers", 
              type: "subcategory",
              description: "Learning from YouTube channels like Traversy Media, Web Dev Simplified, and freeCodeCamp can provide practical tutorials and real-world examples for frontend development."
            },
            { 
              id: "college", 
              name: "College Course work", 
              type: "subcategory",
              description: "Computer Science or Web Development college courses provide structured learning with fundamentals in algorithms, data structures, and software engineering principles."
            },
            { 
              id: "github", 
              name: "Github repositories", 
              type: "subcategory",
              description: "Exploring open-source projects on GitHub offers insights into professional codebases, industry standards, and collaborative development practices."
            },
            { 
              id: "leetcode", 
              name: "Leetcode", 
              type: "subcategory",
              description: "Practicing on platforms like LeetCode helps improve problem-solving skills and algorithm knowledge, which are often tested in technical interviews."
            }
          ]
        },
        {
          id: "self_discovery",
          name: "Self Discovery",
          type: "category",
          description: "Understanding your personal strengths, learning style, and interests helps guide your career path in frontend development and identify specializations that match your abilities.",
          children: [
            { 
              id: "personality", 
              name: "Personality test", 
              type: "subcategory",
              description: "Personality assessments like Myers-Briggs or DISC can help identify how your traits align with different aspects of frontend development, from design-focused to more technical roles."
            },
            { 
              id: "interest", 
              name: "interest survey", 
              type: "subcategory",
              description: "Interest surveys can reveal which areas of frontend development you find most engaging, such as UI design, accessibility, performance optimization, or framework specialization."
            }
          ]
        },
        {
          id: "overview",
          name: "Overview",
          type: "category",
          description: "Frontend development is a rapidly evolving field focused on creating user interfaces for websites and applications, requiring both technical and design skills.",
          children: [
            { 
              id: "job_descriptions", 
              name: "Job Descriptions", 
              type: "subcategory",
              description: "Frontend job descriptions typically require HTML, CSS, JavaScript, and framework experience. They often mention responsive design, cross-browser compatibility, and version control skills."
            },
            { 
              id: "career_path", 
              name: "Career Path Progression", 
              type: "subcategory",
              description: "The frontend career path typically progresses from junior to senior developer, then to lead developer or architect. Some developers specialize in areas like UI/UX or move into management roles."
            }
          ]
        },
        {
          id: "industry",
          name: "Industry",
          type: "category",
          description: "The frontend development industry spans across various sectors including tech companies, agencies, startups, and enterprise organizations, each with their own tech stacks and work environments.",
          children: [
            { 
              id: "historical", 
              name: "Historical Growth", 
              type: "subcategory",
              description: "Frontend development has evolved from basic HTML to complex JavaScript frameworks. The rise of mobile devices created demand for responsive design and progressive web apps."
            },
            { 
              id: "future", 
              name: "Future Outlook", 
              type: "subcategory",
              description: "The future of frontend development includes WebAssembly, AI-assisted coding, headless CMS integrations, and more focus on performance optimization and accessibility."
            }
          ]
        },
        {
          id: "financial",
          name: "Financial Information",
          type: "category",
          description: "Frontend developers typically earn competitive salaries that vary based on experience, location, and specialization. The field offers good financial prospects and job security.",
          children: [
            { 
              id: "salaries", 
              name: "salaries", 
              type: "subcategory",
              description: "Frontend developer salaries typically range from $70,000 for junior roles to $150,000+ for senior positions in the US. Factors affecting salary include location, company size, and specialized skills."
            }
          ]
        }
      ]
    };

    // SVG dimensions
    const width = Math.max(900, window.innerWidth * 0.8);
    const height = Math.max(700, window.innerHeight * 0.7);

    // Create SVG
    const svg = d3.select(svgRef.current)
      .attr("width", "100%")
      .attr("height", "100%")
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("preserveAspectRatio", "xMidYMid meet");
    
    // Create a group for the mind map content that will be zoomed
    const g = svg.append("g")
      .attr("class", "zoomable-group")
      .attr("transform", `translate(${width / 2}, ${height / 2})`);
    
    // Store the group reference
    gRef.current = g.node();

    // Add zoom behavior
    const zoom = d3.zoom()
      .scaleExtent([0.1, 4])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });
    
    // Add a transparent overlay for zoom/pan
    svg.append("rect")
      .attr("width", width)
      .attr("height", height)
      .attr("opacity", 0)
      .attr("pointer-events", "none")
      .attr("class", "zoom-overlay");
    
    // Apply zoom behavior to the SVG itself, not the overlay
    svg.call(zoom as any);
    
    // Add zoom controls (these will stay fixed)
    const zoomControls = svg.append("g")
      .attr("class", "zoom-controls")
      .attr("transform", `translate(${width - 100}, 30)`);
    
    zoomControls.append("rect")
      .attr("width", 30)
      .attr("height", 30)
      .attr("rx", 5)
      .attr("ry", 5)
      .attr("fill", "#f8f9fa")
      .attr("stroke", "#ccc")
      .attr("class", "zoom-in-btn")
      .style("cursor", "pointer")
      .on("click", () => {
        svg.transition().duration(300).call(zoom.scaleBy as any, 1.3);
      });
    
    zoomControls.append("text")
      .attr("x", 15)
      .attr("y", 20)
      .attr("text-anchor", "middle")
      .attr("fill", "#333")
      .style("pointer-events", "none")
      .text("+");
    
    zoomControls.append("rect")
      .attr("width", 30)
      .attr("height", 30)
      .attr("x", 40)
      .attr("rx", 5)
      .attr("ry", 5)
      .attr("fill", "#f8f9fa")
      .attr("stroke", "#ccc")
      .attr("class", "zoom-out-btn")
      .style("cursor", "pointer")
      .on("click", () => {
        svg.transition().duration(300).call(zoom.scaleBy as any, 0.7);
      });
    
    zoomControls.append("text")
      .attr("x", 55)
      .attr("y", 20)
      .attr("text-anchor", "middle")
      .attr("fill", "#333")
      .style("pointer-events", "none")
      .text("-");
    
    zoomControls.append("rect")
      .attr("width", 30)
      .attr("height", 30)
      .attr("x", 80)
      .attr("rx", 5)
      .attr("ry", 5)
      .attr("fill", "#f8f9fa")
      .attr("stroke", "#ccc")
      .attr("class", "zoom-reset-btn")
      .style("cursor", "pointer")
      .on("click", () => {
        svg.transition().duration(300).call(zoom.transform as any, d3.zoomIdentity);
      });
    
    zoomControls.append("text")
      .attr("x", 95)
      .attr("y", 20)
      .attr("text-anchor", "middle")
      .attr("fill", "#333")
      .style("pointer-events", "none")
      .text("⟲");

    // Define colors for each branch
    const colorMap = {
      "skills": "#E57373", // Red
      "self_discovery": "#BA68C8", // Purple
      "overview": "#81C784", // Green
      "industry": "#FFD54F", // Yellow
      "financial": "#FF8A65" // Orange
    };
    
    // Create the mind map layout
    const root = d3.hierarchy(data) as HierarchyNodeWithCoords;
    
    // Position the main node in the center
    root.x = 0;
    root.y = 0;

    // Position the category nodes
    if (root.children) {
      // Skills - top left
      root.children[0].x = -200;
      root.children[0].y = -150;
      
      // Self Discovery - bottom left
      root.children[1].x = -200;
      root.children[1].y = 150;
      
      // Overview - bottom
      root.children[2].x = 0;
      root.children[2].y = 250;
      
      // Industry - top right
      root.children[3].x = 200;
      root.children[3].y = -150;
      
      // Financial Information - right
      root.children[4].x = 200;
      root.children[4].y = 150;
    }

    // Calculate positions for all subcategories first
    if (root.children) {
      root.children.forEach((category) => {
        if (category.children && category.x !== undefined && category.y !== undefined) {
          const subCatCount = category.children.length;
          const gap = 50; // gap between subcategories
          
          category.children.forEach((subcat, subIdx) => {
            // Set position based on parent category
            let x = 0, y = 0;
            
            switch(category.data.id) {
              case "skills": // Skills - to the left
                x = -400;
                y = -200 + subIdx * gap;
                break;
              case "self_discovery": // Self Discovery - bottom left
                x = -400;
                y = 100 + subIdx * gap;
                break;
              case "overview": // Overview - bottom
                x = -100 + subIdx * 200;
                y = 350;
                break;
              case "industry": // Industry - top right
                x = 400;
                y = -200 + subIdx * gap;
                break;
              case "financial": // Financial - right
                x = 400;
                y = 150;
                break;
              default:
                x = category.x;
                y = category.y + (subIdx - (subCatCount - 1) / 2) * gap;
            }
            
            // Position the subcategory node
            (subcat as HierarchyNodeWithCoords).x = x;
            (subcat as HierarchyNodeWithCoords).y = y;
          });
        }
      });
    }

    // Draw all links first (after all positions are calculated)
    root.links().forEach(link => {
      const source = link.source;
      const target = link.target;
      
      // Skip if coordinates are undefined
      if (source.x === undefined || source.y === undefined || 
          target.x === undefined || target.y === undefined) {
        return;
      }

      const sourceX = source.x;
      const sourceY = source.y;
      const targetX = target.x;
      const targetY = target.y;

      const categoryColor = colorMap[source.data.id as keyof typeof colorMap] || 
                          colorMap[target.data.id as keyof typeof colorMap] || 
                          "#555";

      // Draw the link
      g.append("path")
        .attr("class", "link")
        .attr("d", () => {
          // For main to category links, use curved paths
          if (source.data.type === "main") {
            return `M${sourceX},${sourceY}C${(sourceX + targetX) / 2},${sourceY} ${(sourceX + targetX) / 2},${targetY} ${targetX},${targetY}`;
          } 
          // For category to subcategory links, use straight lines
          else {
            return `M${sourceX},${sourceY}L${targetX},${targetY}`;
          }
        })
        .attr("stroke", categoryColor)
        .attr("stroke-width", 2)
        .attr("fill", "none");
    });

    // Function to handle node clicks
    const handleNodeClick = (event: MouseEvent, d: HierarchyNodeWithCoords) => {
      // Get mouse position relative to svg
      const svgElement = svgRef.current;
      const transform = gRef.current ? d3.zoomTransform(gRef.current) : d3.zoomIdentity;
      
      if (svgElement) {
        const svgRect = svgElement.getBoundingClientRect();
        const popupX = event.clientX - svgRect.left + 20; // Offset to not cover the node
        const popupY = event.clientY - svgRect.top;
        
        setPopup({
          node: d.data,
          position: { x: popupX, y: popupY }
        });
      }
      
      // Stop propagation to prevent zoom/pan
      event.stopPropagation();
    };

    // Now draw all nodes
    const nodes = g.selectAll(".node")
      .data(root.descendants())
      .enter()
      .append("g")
      .attr("class", d => `node ${d.data.type}`)
      .attr("transform", d => `translate(${d.x},${d.y})`)
      .style("cursor", "pointer")
      .on("click", handleNodeClick);

    // Add rectangles for main node
    nodes.filter(d => d.data.type === "main")
      .append("rect")
      .attr("width", d => d.data.name.length * 10 + 20)
      .attr("height", 40)
      .attr("x", d => -(d.data.name.length * 10 + 20) / 2)
      .attr("y", -20)
      .attr("rx", 5)
      .attr("ry", 5)
      .attr("fill", "#FFFFFF")
      .attr("stroke", "#555")
      .attr("stroke-width", 1)
      .attr("class", "clickable-node");

    // Add text to main node
    nodes.filter(d => d.data.type === "main")
      .append("text")
      .attr("dy", 5)
      .attr("text-anchor", "middle")
      .text(d => d.data.name)
      .attr("fill", "#333");

    // Add category nodes with their specific colors
    nodes.filter(d => d.data.type === "category")
      .each(function(d) {
        const nodeColor = colorMap[d.data.id as keyof typeof colorMap] || "#CCCCCC";
        const node = d3.select(this);
        
        // Add rectangle for category node
        node.append("rect")
          .attr("width", d.data.name.length * 10 + 20)
          .attr("height", 30)
          .attr("x", -(d.data.name.length * 10 + 20) / 2)
          .attr("y", -15)
          .attr("rx", 5)
          .attr("ry", 5)
          .attr("fill", "#FFFFFF")
          .attr("stroke", nodeColor)
          .attr("stroke-width", 1)
          .attr("class", "clickable-node");
        
        node.append("text")
          .attr("dy", 5)
          .attr("text-anchor", "middle")
          .text(d.data.name)
          .attr("fill", "#333");
      });

    // Draw subcategory nodes
    if (root.children) {
      root.children.forEach((category) => {
        if (category.children && category.x !== undefined && category.y !== undefined) {
          const categoryColor = colorMap[category.data.id as keyof typeof colorMap] || "#CCCCCC";
          
          category.children.forEach((subcat) => {
            const x = (subcat as HierarchyNodeWithCoords).x;
            const y = (subcat as HierarchyNodeWithCoords).y;
            
            // Draw the node
            const subG = g.append("g")
              .attr("transform", `translate(${x}, ${y})`)
              .attr("class", "subcat-node")
              .style("cursor", "pointer")
              .on("click", (event) => handleNodeClick(event, subcat as HierarchyNodeWithCoords));
            
            // Add rectangle for subcategory node
            subG.append("rect")
              .attr("width", subcat.data.name.length * 10 + 20)
              .attr("height", 30)
              .attr("x", -(subcat.data.name.length * 10 + 20) / 2)
              .attr("y", -15)
              .attr("rx", 5)
              .attr("ry", 5)
              .attr("fill", "#FFFFFF")
              .attr("stroke", categoryColor)
              .attr("stroke-width", 1)
              .attr("class", "clickable-node");
            
            subG.append("text")
              .attr("text-anchor", "middle")
              .attr("dy", 5)
              .text(subcat.data.name)
              .attr("fill", "#333");
          });
        }
      });
    }

    // Add instructions for zoom/pan
    svg.append("text")
      .attr("x", 20)
      .attr("y", 30)
      .attr("fill", "#666")
      .attr("font-size", "12px")
      .attr("pointer-events", "none")
      .text("Tip: Use mouse wheel to zoom, drag to pan");
  };

  useEffect(() => {
    renderMindMap();

    // Add resize event listener
    const handleResize = () => {
      renderMindMap();
    };

    window.addEventListener('resize', handleResize);

    // Clean up
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <div className="mind-map-container">
      <svg ref={svgRef}></svg>
      {popup && (
        <Popup 
          node={popup.node} 
          position={popup.position}
          onClose={() => setPopup(null)}
        />
      )}
    </div>
  );
};

export default MindMapGD; 