import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  ArrowLeft, 
  MapPin, 
  User, 
  Star,
  ShoppingCart,
  Calendar
} from 'lucide-react'

const EquipmentDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { apiCall, isAuthenticated } = useAuth()
  const [equipment, setEquipment] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchEquipment()
  }, [id])

  const fetchEquipment = async () => {
    const result = await apiCall(`/equipment/${id}`)
    if (result.success) {
      setEquipment(result.data)
    }
    setLoading(false)
  }

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD'
    }).format(price)
  }

  const handleTransaction = (type) => {
    if (!isAuthenticated) {
      navigate('/login')
      return
    }
    // Aquí iría la lógica para crear transacción
    alert(`Funcionalidad de ${type} en desarrollo`)
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-orange-600"></div>
      </div>
    )
  }

  if (!equipment) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Equipo no encontrado</h2>
        <Button onClick={() => navigate('/equipment')}>
          Volver al catálogo
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <Button 
        variant="ghost" 
        onClick={() => navigate('/equipment')}
        className="flex items-center"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Volver al catálogo
      </Button>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Images */}
        <div>
          <div className="aspect-square bg-gray-200 rounded-lg flex items-center justify-center">
            {equipment.images && equipment.images.length > 0 ? (
              <img 
                src={equipment.images[0]} 
                alt={equipment.title}
                className="w-full h-full object-cover rounded-lg"
              />
            ) : (
              <div className="text-gray-400">Sin imagen disponible</div>
            )}
          </div>
        </div>

        {/* Details */}
        <div className="space-y-6">
          <div>
            <div className="flex items-center justify-between mb-2">
              <h1 className="text-3xl font-bold text-gray-800">{equipment.title}</h1>
              <Badge variant="outline">{equipment.category}</Badge>
            </div>
            <p className="text-gray-600">{equipment.description}</p>
          </div>

          {/* Owner Info */}
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center space-x-3">
                <User className="h-8 w-8 text-gray-400" />
                <div>
                  <p className="font-semibold">{equipment.owner_name}</p>
                  <div className="flex items-center">
                    <Star className="h-4 w-4 text-yellow-400 fill-current mr-1" />
                    <span className="text-sm text-gray-600">Propietario verificado</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Location */}
          {equipment.location && (
            <div className="flex items-center text-gray-600">
              <MapPin className="h-5 w-5 mr-2" />
              {equipment.location}
            </div>
          )}

          {/* Pricing */}
          <Card>
            <CardHeader>
              <CardTitle>Precios y Disponibilidad</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {equipment.is_for_sale && equipment.price_sale && (
                <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
                  <div>
                    <p className="font-semibold text-green-800">Venta</p>
                    <p className="text-2xl font-bold text-green-600">
                      {formatPrice(equipment.price_sale)}
                    </p>
                  </div>
                  <Button 
                    className="bg-green-600 hover:bg-green-700"
                    onClick={() => handleTransaction('compra')}
                    disabled={equipment.availability_status !== 'available'}
                  >
                    <ShoppingCart className="h-4 w-4 mr-2" />
                    Comprar
                  </Button>
                </div>
              )}

              {equipment.is_for_rent && (
                <div className="space-y-3">
                  {equipment.price_rent_daily && (
                    <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
                      <div>
                        <p className="font-semibold text-blue-800">Renta Diaria</p>
                        <p className="text-2xl font-bold text-blue-600">
                          {formatPrice(equipment.price_rent_daily)}/día
                        </p>
                      </div>
                      <Button 
                        className="bg-blue-600 hover:bg-blue-700"
                        onClick={() => handleTransaction('renta diaria')}
                        disabled={equipment.availability_status !== 'available'}
                      >
                        <Calendar className="h-4 w-4 mr-2" />
                        Rentar
                      </Button>
                    </div>
                  )}

                  {equipment.price_rent_weekly && (
                    <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
                      <div>
                        <p className="font-semibold text-blue-800">Renta Semanal</p>
                        <p className="text-2xl font-bold text-blue-600">
                          {formatPrice(equipment.price_rent_weekly)}/semana
                        </p>
                      </div>
                      <Button 
                        className="bg-blue-600 hover:bg-blue-700"
                        onClick={() => handleTransaction('renta semanal')}
                        disabled={equipment.availability_status !== 'available'}
                      >
                        <Calendar className="h-4 w-4 mr-2" />
                        Rentar
                      </Button>
                    </div>
                  )}
                </div>
              )}

              {equipment.availability_status !== 'available' && (
                <div className="p-4 bg-gray-50 rounded-lg text-center">
                  <p className="text-gray-600">
                    Este equipo no está disponible actualmente
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Specifications */}
          {equipment.specifications && Object.keys(equipment.specifications).length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Especificaciones</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {Object.entries(equipment.specifications).map(([key, value]) => (
                    <div key={key} className="flex justify-between">
                      <span className="text-gray-600">{key}:</span>
                      <span className="font-semibold">{value}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

export default EquipmentDetail

