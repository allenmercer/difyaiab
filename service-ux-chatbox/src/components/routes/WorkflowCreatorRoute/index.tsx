import ChatBot from '../../chatbot/ChatBot';
import FilePicker from '../../file-picker/FilePicker';
import WorkFlows from '../../../components/workflows/WorkFlows';

const WorkflowCreator = () => {
  return (
    <>
      <div className='flex bg-[#808080]'>
        <WorkFlows />

        <div className='flex-col bg-black w-5/6'>
          <div
            className='flex pt-6 pr-6'
            style={{ justifyContent: 'flex-end' }}>
            <FilePicker />
          </div>
          <ChatBot />
          {/* <div className='flex justify-center p-2 bg-black'>
            <FilePicker />
          </div> */}
        </div>
      </div>
    </>
  );
};

export default WorkflowCreator;
