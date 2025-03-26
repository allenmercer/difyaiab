import { useEffect, useState } from 'react';
import axios from 'axios';

interface WorkflowResponse {
  workflows: string[];
}

const WorkFlows = () => {
  const [workflows, setWorkflows] = useState<string[]>([]);
  const payload = {
    email: import.meta.env.VITE_EMAIL,
    password: import.meta.env.VITE_PASSWORD,
  };
  const config = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  useEffect(() => {
    const fetchWorkflows = async () => {
      try {
        const response = await axios.post(
          `${import.meta.env.VITE_BACKEND}/api/v1/workflows`,
          payload,
          config
        );
        const parsedObject: WorkflowResponse = response.data;

        if (Array.isArray(parsedObject.workflows)) {
          setWorkflows(parsedObject.workflows);
        } else {
          console.error('Invalid workflows data:', parsedObject.workflows);
        }
      } catch (error) {
        console.error('Error fetching workflows:', error);
      }
    };

    fetchWorkflows();

    const intervalId = setInterval(fetchWorkflows, 30000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className='flex-col w-1/6 text-white' style={{ height: '100vh' }}>
      <h2 className='m-4 flex justify-center text-2xl'>Workflows</h2>
      {workflows.length === 0 ?
        <div className='p-2 m-4 flex justify-start'>No workflows found.</div>
      : <div className='items-start'>
          {workflows.map((workflow, index) => (
            <h2 key={index} className='p-2 ml-4 flex justify-start text-bold'>
              {workflow}
            </h2>
          ))}
        </div>
      }
    </div>
  );
};

export default WorkFlows;
