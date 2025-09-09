import { useAuth } from '../contexts/AuthContext'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  User, 
  Package, 
  ShoppingCart, 
  DollarSign,
  Star,
  Settings
} from 'lucide-react'

const Dashboard = () => {
  const { user } = useAuth()

  const getUserTypeBadge = (type) => {
    const variants = {
      owner: 'bg-blue-100 text-blue-800',
      renter: 'bg-green-100 text-green-800',
      both: 'bg-purple-100 text-purple-800'
    }
    
    const labels = {
      owner: 'Propietario',
      renter: 'Arrendatario',
      both: 'Propietario y Arrendatario'
    }

    return (
      <Badge className={variants[type]}>
        {labels[type]}
      </Badge>
    )
  }

  const getVerificationBadge = (status) => {
    const variants = {
      pending: 'bg-yellow-100 text-yellow-800',
      verified: 'bg-green-100 text-green-800',
      rejected: 'bg-red-100 text-red-800'
    }
    
    const labels = {
      pending: 'Pendiente',
      verified: 'Verificado',
      rejected: 'Rechazado'
    }

    return (
      <Badge className={variants[status]}>
        {labels[status]}
      </Badge>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-800">Mi Panel</h1>
        <p className="text-gray-600">Gestiona tu perfil y actividad en Topke MarkePlace</p>
      </div>

      {/* User Profile Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <User className="h-5 w-5 mr-2" />
            Información del Perfil
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-600">Nombre</label>
                <p className="text-lg font-semibold">{user?.name}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Email</label>
                <p className="text-lg">{user?.email}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Teléfono</label>
                <p className="text-lg">{user?.phone || 'No especificado'}</p>
              </div>
            </div>
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-600">Tipo de Usuario</label>
                <div className="mt-1">
                  {getUserTypeBadge(user?.user_type)}
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Estado de Verificación</label>
                <div className="mt-1">
                  {getVerificationBadge(user?.verification_status)}
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Calificación</label>
                <div className="flex items-center mt-1">
                  <Star className="h-5 w-5 text-yellow-400 fill-current mr-1" />
                  <span className="text-lg font-semibold">{user?.rating || 0}</span>
                  <span className="text-gray-600 ml-1">/5</span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <Package className="h-8 w-8 text-blue-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Mis Equipos</p>
                <p className="text-2xl font-bold">0</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <ShoppingCart className="h-8 w-8 text-green-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Compras</p>
                <p className="text-2xl font-bold">0</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <DollarSign className="h-8 w-8 text-orange-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Ventas</p>
                <p className="text-2xl font-bold">0</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <Star className="h-8 w-8 text-yellow-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Reseñas</p>
                <p className="text-2xl font-bold">0</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Acciones Rápidas</CardTitle>
          <CardDescription>
            Gestiona tu actividad en la plataforma
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 border rounded-lg hover:bg-gray-50 cursor-pointer">
              <Package className="h-8 w-8 text-blue-600 mb-2" />
              <h3 className="font-semibold">Mis Equipos</h3>
              <p className="text-sm text-gray-600">Ver y gestionar tus equipos publicados</p>
            </div>
            <div className="p-4 border rounded-lg hover:bg-gray-50 cursor-pointer">
              <ShoppingCart className="h-8 w-8 text-green-600 mb-2" />
              <h3 className="font-semibold">Mis Transacciones</h3>
              <p className="text-sm text-gray-600">Historial de compras y ventas</p>
            </div>
            <div className="p-4 border rounded-lg hover:bg-gray-50 cursor-pointer">
              <Settings className="h-8 w-8 text-gray-600 mb-2" />
              <h3 className="font-semibold">Configuración</h3>
              <p className="text-sm text-gray-600">Actualizar perfil y preferencias</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Dashboard

