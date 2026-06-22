import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/clerk-react";
import { Button } from "@/components/ui/button";
import { CustomerForm } from "@/components/CustomerForm"; // Importe seu novo formulário

function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-zinc-50 p-4">
      
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
        <div className="w-full max-w-md flex flex-col items-center space-y-6">
          <div className="flex items-center gap-4 bg-white p-4 rounded-lg shadow-sm border w-full justify-between">
            <span className="font-medium">Bem-vindo(a)!</span>
            <UserButton />
          </div>
          
          {/* O formulário de dados só aparece aqui */}
          <CustomerForm />
        </div>
      </SignedIn>
      
    </div>
  );
}

export default App;