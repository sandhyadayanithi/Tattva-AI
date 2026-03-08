<<<<<<< HEAD
import { RouterProvider } from "react-router";
import { router } from "./routes";
import { Toaster } from "./components/ui/sonner";

export default function App() {
  return (
    <>
      <RouterProvider router={router} />
      <Toaster />
    </>
  );
}
=======
import { RouterProvider } from 'react-router';
import { router } from './routes';

function App() {
  return <RouterProvider router={router} />;
}

export default App;
>>>>>>> 009a52ca1ffae4c2f23641b736d59688f7687a9b
