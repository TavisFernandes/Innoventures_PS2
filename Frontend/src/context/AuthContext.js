'use client';

import { createContext, useContext, useEffect, useState } from 'react';

const AuthContext = createContext();

export function useAuth() {
  const context = useContext(AuthContext);
  // Return default values during SSR
  if (!context) {
    return {
      user: null,
      loading: true,
      signInWithGoogle: () => {},
      signOut: () => {}
    };
  }
  return context;
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate authentication state
    setLoading(false);
  }, []);

  const signInWithGoogle = async () => {
    // Mock sign in - set a mock user
    const mockUser = {
      uid: 'demo-user-123',
      email: 'demo@example.com',
      displayName: 'Demo User'
    };
    setUser(mockUser);
    console.log('Mock sign-in successful:', mockUser);
  };

  const signOutUser = async () => {
    setUser(null);
    console.log('Mock sign out successful');
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
