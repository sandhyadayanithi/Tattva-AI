import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// TODO: Replace with your actual Firebase config from the Firebase Console
const firebaseConfig = {
    apiKey: "AIzaSyCO2iHqkw72Vt9ecaqINoAO3OkWW9WEtJM",
    authDomain: "tattva-ai.firebaseapp.com",
    projectId: "tattva-ai",
    storageBucket: "tattva-ai.firebasestorage.app",
    messagingSenderId: "387237236754",
    appId: "1:387237236754:web:0aaab3ee6d8f5dec1088cb"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
export const googleProvider = new GoogleAuthProvider();
