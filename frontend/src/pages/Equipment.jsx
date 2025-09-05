import { useState, useEffect } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { 
  Search, 
  Filter, 
  MapPin, 
  Calendar,
  DollarSign,
  Star,
  Eye
} from 'lucide-react'

const Equipment = () => {
  const [equipment, setEquipment] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    search: '',
    category: '',
    location: '',
    type: '',
    min_price: '',
    max_price: ''
  })
  const [searchParams, setSearchParams] = useSearchParams()

  const { apiCall } = useAuth()

  useEffect(() => {
    // Obtener filtros de URL
    const category = searchParams.get('category')
    if (category) {
      setFilters(prev => ({ ...prev, category }))
    }
    
    fetchCategories()
    fetchEquipment()
  }, [])

  useEffect(() => {
    fetchEquipment()
  }, [filters])

  const fetchCategories = async () => {
    const result = await apiCall('/equipment/categories')
    if (result.success) {
      setCategories(result.data.categories)
    }
  }

  const fetchEquipment = async () => {
    setLoading(true)
    const params = new URLSearchParams()
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.append(key, value)
    })

    const result = await apiCall(`/equipment?${params.toString()}`)
    if (result.success) {
      setEquipment(result.data.equipment)
    }
    setLoading(false)
  }

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }))
  }

  const clearFilters = () => {
    setFilters({
      search: '',
      category: '',
      location: '',
      type: '',
      min_price: '',
      max_price: ''
    })
    setSearchParams({})
  }

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD'
    }).format(price)
  }

  const getAvailabilityBadge = (status) => {
    const variants = {
      available: 'bg-green-100 text-green-800',
      rented: 'bg-yellow-100 text-yellow-800',
      sold: 'bg-red-100 text-red-800',
      maintenance: 'bg-gray-100 text-gray-800'
    }
    
    const labels = {
      available: 'Disponible',
      rented: 'Rentado',
      sold: 'Vendido',
      maintenance: 'Mantenimiento'
    }

    return (
      <Badge className={variants[status]}>
        {labels[status]}
      </Badge>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Catálogo de Equipos</h1>
          <p className="text-gray-600">Encuentra la maquinaria perfecta para tu proyecto</p>
        </div>
        <Link to="/add-equipment">
          <Button className="bg-orange-600 hover:bg-orange-700">
            Publicar Equipo
          </Button>
        </Link>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Filter className="h-5 w-5 mr-2" />
            Filtros de Búsqueda
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
            <div className="xl:col-span-2">
              <Input
                placeholder="Buscar equipos..."
                value={filters.search}
                onChange={(e) => handleFilterChange('search', e.target.value)}
                className="w-full"
              />
            </div>
            
            <Select value={filters.category} onValueChange={(value) => handleFilterChange('category', value)}>
              <SelectTrigger>
                <SelectValue placeholder="Categoría" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Todas las categorías</SelectItem>
                {categories.map(category => (
                  <SelectItem key={category} value={category}>
                    {category}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Input
              placeholder="Ubicación"
              value={filters.location}
              onChange={(e) => handleFilterChange('location', e.target.value)}
            />

            <Select value={filters.type} onValueChange={(value) => handleFilterChange('type', value)}>
              <SelectTrigger>
                <SelectValue placeholder="Tipo" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Venta y Renta</SelectItem>
                <SelectItem value="sale">Solo Venta</SelectItem>
                <SelectItem value="rent">Solo Renta</SelectItem>
              </SelectContent>
            </Select>

            <Button 
              variant="outline" 
              onClick={clearFilters}
              className="w-full"
            >
              Limpiar Filtros
            </Button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
            <Input
              placeholder="Precio mínimo"
              type="number"
              value={filters.min_price}
              onChange={(e) => handleFilterChange('min_price', e.target.value)}
            />
            <Input
              placeholder="Precio máximo"
              type="number"
              value={filters.max_price}
              onChange={(e) => handleFilterChange('max_price', e.target.value)}
            />
          </div>
        </CardContent>
      </Card>

      {/* Equipment Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <div className="h-48 bg-gray-200 rounded-t-lg"></div>
              <CardContent className="p-4">
                <div className="h-4 bg-gray-200 rounded mb-2"></div>
                <div className="h-3 bg-gray-200 rounded mb-4"></div>
                <div className="h-6 bg-gray-200 rounded"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : equipment.length === 0 ? (
        <Card>
          <CardContent className="text-center py-12">
            <Search className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              No se encontraron equipos
            </h3>
            <p className="text-gray-600">
              Intenta ajustar los filtros de búsqueda
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {equipment.map((item) => (
            <Card key={item.id} className="hover:shadow-lg transition-shadow">
              <div className="relative">
                <div className="h-48 bg-gray-200 rounded-t-lg flex items-center justify-center">
                  {item.images && item.images.length > 0 ? (
                    <img 
                      src={item.images[0]} 
                      alt={item.title}
                      className="w-full h-full object-cover rounded-t-lg"
                    />
                  ) : (
                    <div className="text-gray-400">Sin imagen</div>
                  )}
                </div>
                <div className="absolute top-2 right-2">
                  {getAvailabilityBadge(item.availability_status)}
                </div>
              </div>
              
              <CardContent className="p-4">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-semibold text-lg truncate">{item.title}</h3>
                  <Badge variant="outline">{item.category}</Badge>
                </div>
                
                <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                  {item.description}
                </p>

                {item.location && (
                  <div className="flex items-center text-sm text-gray-500 mb-2">
                    <MapPin className="h-4 w-4 mr-1" />
                    {item.location}
                  </div>
                )}

                <div className="flex items-center text-sm text-gray-500 mb-3">
                  <Star className="h-4 w-4 mr-1 fill-current text-yellow-400" />
                  {item.owner_name}
                </div>

                <div className="space-y-2 mb-4">
                  {item.is_for_sale && item.price_sale && (
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Venta:</span>
                      <span className="font-semibold text-green-600">
                        {formatPrice(item.price_sale)}
                      </span>
                    </div>
                  )}
                  {item.is_for_rent && (
                    <div className="space-y-1">
                      {item.price_rent_daily && (
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600">Renta/día:</span>
                          <span className="font-semibold text-blue-600">
                            {formatPrice(item.price_rent_daily)}
                          </span>
                        </div>
                      )}
                      {item.price_rent_weekly && (
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600">Renta/semana:</span>
                          <span className="font-semibold text-blue-600">
                            {formatPrice(item.price_rent_weekly)}
                          </span>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                <Link to={`/equipment/${item.id}`}>
                  <Button className="w-full" variant="outline">
                    <Eye className="h-4 w-4 mr-2" />
                    Ver Detalles
                  </Button>
                </Link>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

export default Equipment

