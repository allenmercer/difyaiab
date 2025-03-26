import { Link } from '@tanstack/react-router';

export default function MainNavigation() {
  return (
    <div
      className='flex justify-start space-x-4'
      style={{ padding: '1em 0 1em 4em' }}>
      <Link
        to='/'
        className='[&.active]:text-blue-500 [&.active]:border-b-2 [&.active]:border-blue-500 [&.active]:rounded-none px-4 py-2 border-white rounded-none text-gray-70 hover:bg-blue-300 font-bold border-b-2 transition duration-300 ease-in-out'>
        Workflow Creator
      </Link>{' '}
      <Link
        to='/agent-builder'
        className='[&.active]:text-blue-500 [&.active]:border-b-2 [&.active]:border-blue-500 [&.active]:rounded-none px-4 py-2 border-white text-gray-70 hover:bg-blue-300 font-bold border-b-2 transition duration-300 ease-in-out'>
        Agent Builder
      </Link>{' '}
    </div>
  );
}
