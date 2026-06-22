import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/clerk-react";
import { Button } from "@/components/ui/button";

function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-zinc-50">
      
      {/* O que aparece quando a pessoa NÃO está logada */}
      <SignedOut>
        <div className="text-center space-y-4 bg-white p-8 rounded-xl shadow-sm border border-zinc-200">
          <h1 className="text-3xl font-bold text-zinc-900">Salão da Leila</h1>
          <p className="text-zinc-500">Faça login para agendar seu horário</p>
          
          <SignInButton mode="modal">
            <Button className="w-full">Entrar / Cadastrar</Button>
          </SignInButton>
        </div>
      </SignedOut>

      {/* O que aparece quando a pessoa ESTÁ logada */}
      <SignedIn>
        <div className="text-center space-y-4 bg-white p-8 rounded-xl shadow-sm border border-zinc-200 flex flex-col items-center">
          <UserButton />
          <h1 className="text-2xl font-bold text-zinc-900">Bem-vindo(a)!</h1>
          <p className="text-zinc-500">Você está logado e pronto para agendar.</p>
        </div>
      </SignedIn>
      
    </div>
  );
}

export default App;