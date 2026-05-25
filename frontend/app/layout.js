import './globals.css';

export const metadata = {
  title: 'Student Management System',
  description: 'Modern student registration and management dashboard',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
