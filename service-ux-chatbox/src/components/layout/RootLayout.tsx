import { Outlet } from '@tanstack/react-router';
import MainNavigation from '../navigation/MainNavigation';
import Header from '../header/Header';
import Footer from '../footer/Footer';

/**
 * Root layout wrapping the whole app.
 */
export default function RootLayout() {
  return (
    <>
      <Header />
      <MainNavigation />
      <hr />
      <Outlet />
      <Footer />
    </>
  );
}
