import React from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";

function TeamMemberCard({ name, role, responsibilities, tasks }) {
  return (
    <Card className="w-96 shadow-lg rounded-2xl p-4">
      <CardContent>
        <h2 className="text-xl font-bold mb-2">{name}</h2>
        <p className="text-lg text-blue-600 mb-2">{role}</p>
        <p className="font-semibold mb-2">Responsibilities:</p>
        <ul className="list-disc pl-5 mb-4">
          {responsibilities.map((item, index) => (
            <li key={index} className="mb-1">{item}</li>
          ))}
        </ul>
        <p className="font-semibold mb-2">Tasks:</p>
        <ul className="list-disc pl-5">
          {tasks.map((task, index) => (
            <li key={index} className="mb-1">{task}</li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}

export default function ConstructionSite() {
  return (
    <div className="h-screen w-full bg-gray-100">
      <Canvas className="h-1/2 bg-gray-300 rounded-lg shadow-inner">
        {/* Placeholder for 3D Models */}
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <mesh position={[0, 0, 0]}>
          <boxGeometry args={[1, 1, 1]} />
          <meshStandardMaterial color="orange" />
        </mesh>
        <OrbitControls />
      </Canvas>
      <div className="p-6 grid gap-6 grid-cols-1 md:grid-cols-3">
        <motion.div
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <TeamMemberCard
            name="Team Member 1: Backend Developer"
            role="- Develop API integration and backend logic."
            responsibilities={["Handle data fetching, cleaning, and preprocessing.", "Implement budget and risk analysis logic."]}
            tasks={["Create accuweather.py for weather data integration.", "Write gpt_utils.py for AI-based suggestions.", "Work on data_handler.py for data preprocessing.", "Develop logic in budget_model.py and risk_analysis.py."]}
          />
        </motion.div>
        <motion.div
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <TeamMemberCard
            name="Team Member 2: Frontend/Visualization"
            role="- Build dashboard and graphs."
            responsibilities={["Handle UI/UX for insights.", "Link frontend with backend APIs."]}
            tasks={["Work on dashboard.py for the user interface.", "Write visualization functions in graphs.py.", "Integrate weather and budget insights into the dashboard."]}
          />
        </motion.div>
        <motion.div
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <TeamMemberCard
            name="Team Member 3: Testing & Documentation"
            role="- Write test scripts for APIs, models, and UI."
            responsibilities={["Document project requirements and API usage.", "Set up project environment and ensure smooth deployment."]}
            tasks={["Create unit tests in tests/ folder.", "Write requirements.md and api_usage.md in docs/.", "Set up .env and ensure dependencies in requirements.txt.", "Assist with debugging and deployment."]}
          />
        </motion.div>
      </div>
    </div>
  );
}
