'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged } from 'firebase/auth';
import { firebaseConfig } from '@/config/firebase';

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Initialize Firebase immediately when AuthProvider mounts
    import('@/lib/firebaseInit').then(() => {
      // Firebase is now initialized, set up auth listener
      const unsubscribe = onAuthStateChanged(getAuth(), (user) => {
        setUser(user);
        setLoading(false);
      });

      return unsubscribe;
    }).catch(error => {
      console.error('Firebase initialization error:', error);
      setLoading(false);
    });
  }, []);

  const signInWithGoogle = async () => {
    try {
      const provider = new GoogleAuthProvider();
      const result = await signInWithPopup(getAuth(), provider);
      console.log('Google sign-in successful:', result.user);
    } catch (error) {
      console.error('Error signing in with Google:', error);
    }
  };

  const signOutUser = async () => {
    try {
      await signOut(getAuth());
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  const value = {
    user,
    loading,
    signInWithGoogle,
    signOut: signOutUser
  };

  console.log('AuthContext value:', value);

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
