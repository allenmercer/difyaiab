const Header = () => {
  return (
    <div className='flex row justify-center w-full bg-gray-200'>
      <img
        src='path/to/your/image.png'
        alt='Logo Placeholder'
        className='h-8 w-8 pr-4'
      />
      <div
        className='text-xl font-bold bg-gray-200 ml-4'
        style={{ padding: '1em' }}>
        [AI]levate Agent Builder
      </div>
    </div>
  );
};

export default Header;
