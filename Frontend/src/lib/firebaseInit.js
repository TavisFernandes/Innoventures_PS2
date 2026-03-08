import { initializeApp, getApps } from 'firebase/app';
import { firebaseConfig } from '@/config/firebase';

// Initialize Firebase app only on client side
let app = null;

// Only initialize on client side (browser)
if (typeof window !== 'undefined') {
  const existingApps = getApps();
  if (existingApps.length === 0) {
    try {
      app = initializeApp(firebaseConfig);
      console.log('Firebase app initialized successfully');
    } catch (error) {
      console.error('Firebase initialization error:', error);
      // Create a minimal app for basic functionality
      app = initializeApp({
        apiKey: firebaseConfig.apiKey,
        authDomain: firebaseConfig.authDomain,
        projectId: firebaseConfig.projectId,
        appId: firebaseConfig.appId
      });
      console.log('Firebase app initialized with minimal config');
    }
  } else {
    app = getApps()[0];
    console.log('Using existing Firebase app');
  }
}

export { app };
