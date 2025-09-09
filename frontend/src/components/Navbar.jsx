import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuTrigger 
} from '@/components/ui/dropdown-menu'
import { 
  User, 
  LogOut, 
  Settings, 
  Plus, 
  FileText, 
  Shield,
  Construction,
  Menu
} from 'lucide-react'

const Navbar = () => {
  const { user, logout, isAuthenticated, isAdmin } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <nav className="bg-white shadow-lg border-b">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <Construction className="h-8 w-8 text-orange-600" />
            <span className="text-xl font-bold text-gray-800">Topke MarkePlace</span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-6">
            <Link 
              to="/equipment" 
              className="text-gray-600 hover:text-orange-600 transition-colors"
            >
              Equipos
            </Link>
            
            {isAuthenticated ? (
              <>
                <Link 
                  to="/dashboard" 
                  className="text-gray-600 hover:text-orange-600 transition-colors"
                >
                  Mi Panel
                </Link>
                <Link 
                  to="/add-equipment" 
                  className="text-gray-600 hover:text-orange-600 transition-colors"
                >
                  Publicar Equipo
                </Link>
                <Link 
                  to="/transactions" 
                  className="text-gray-600 hover:text-orange-600 transition-colors"
                >
                  Transacciones
                </Link>
                
                {/* User Menu */}
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" className="flex items-center space-x-2">
                      <User className="h-4 w-4" />
                      <span>{user?.name}</span>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end" className="w-48">
                    <DropdownMenuItem onClick={() => navigate('/dashboard')}>
                      <Settings className="h-4 w-4 mr-2" />
                      Mi Perfil
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => navigate('/add-equipment')}>
                      <Plus className="h-4 w-4 mr-2" />
                      Publicar Equipo
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => navigate('/transactions')}>
                      <FileText className="h-4 w-4 mr-2" />
                      Mis Transacciones
                    </DropdownMenuItem>
                    {isAdmin && (
                      <DropdownMenuItem onClick={() => navigate('/admin')}>
                        <Shield className="h-4 w-4 mr-2" />
                        Panel Admin
                      </DropdownMenuItem>
                    )}
                    <DropdownMenuItem onClick={handleLogout} className="text-red-600">
                      <LogOut className="h-4 w-4 mr-2" />
                      Cerrar Sesión
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </>
            ) : (
              <div className="flex items-center space-x-4">
                <Link to="/login">
                  <Button variant="ghost">Iniciar Sesión</Button>
                </Link>
                <Link to="/register">
                  <Button className="bg-orange-600 hover:bg-orange-700">
                    Registrarse
                  </Button>
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu */}
          <div className="md:hidden">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="sm">
                  <Menu className="h-5 w-5" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48">
                <DropdownMenuItem onClick={() => navigate('/equipment')}>
                  Equipos
                </DropdownMenuItem>
                {isAuthenticated ? (
                  <>
                    <DropdownMenuItem onClick={() => navigate('/dashboard')}>
                      Mi Panel
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => navigate('/add-equipment')}>
                      Publicar Equipo
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => navigate('/transactions')}>
                      Transacciones
                    </DropdownMenuItem>
                    {isAdmin && (
                      <DropdownMenuItem onClick={() => navigate('/admin')}>
                        Panel Admin
                      </DropdownMenuItem>
                    )}
                    <DropdownMenuItem onClick={handleLogout} className="text-red-600">
                      Cerrar Sesión
                    </DropdownMenuItem>
                  </>
                ) : (
                  <>
                    <DropdownMenuItem onClick={() => navigate('/login')}>
                      Iniciar Sesión
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => navigate('/register')}>
                      Registrarse
                    </DropdownMenuItem>
                  </>
                )}
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar

