import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { 
  Construction, 
  Users, 
  Shield, 
  TrendingUp,
  Search,
  Plus,
  Star
} from 'lucide-react'

const Home = () => {
  const features = [
    {
      icon: <Construction className="h-8 w-8 text-orange-600" />,
      title: "Amplio Catálogo",
      description: "Miles de equipos de construcción disponibles para venta y renta"
    },
    {
      icon: <Users className="h-8 w-8 text-orange-600" />,
      title: "Comunidad Confiable",
      description: "Usuarios verificados con sistema de calificaciones y reseñas"
    },
    {
      icon: <Shield className="h-8 w-8 text-orange-600" />,
      title: "Transacciones Seguras",
      description: "Plataforma segura con protección para compradores y vendedores"
    },
    {
      icon: <TrendingUp className="h-8 w-8 text-orange-600" />,
      title: "Mejores Precios",
      description: "Encuentra las mejores ofertas del mercado con precios competitivos"
    }
  ]

  const categories = [
    "Excavadoras",
    "Bulldozers", 
    "Grúas",
    "Cargadores",
    "Compactadores",
    "Generadores"
  ]

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center py-20 bg-gradient-to-r from-orange-50 to-orange-100 rounded-lg">
        <div className="max-w-4xl mx-auto px-4">
          <h1 className="text-5xl font-bold text-gray-800 mb-6">
            El Marketplace Líder en 
            <span className="text-orange-600"> Maquinaria de Construcción</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Compra, vende o renta equipos de construcción de manera fácil y segura. 
            Conectamos a propietarios con quienes necesitan maquinaria especializada.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/equipment">
              <Button size="lg" className="bg-orange-600 hover:bg-orange-700">
                <Search className="h-5 w-5 mr-2" />
                Explorar Equipos
              </Button>
            </Link>
            <Link to="/register">
              <Button size="lg" variant="outline" className="border-orange-600 text-orange-600 hover:bg-orange-50">
                <Plus className="h-5 w-5 mr-2" />
                Publicar Equipo
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section>
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-800 mb-4">
            ¿Por qué elegir ConstructMarket?
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Somos la plataforma más confiable para transacciones de maquinaria de construcción
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <Card key={index} className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex justify-center mb-4">
                  {feature.icon}
                </div>
                <CardTitle className="text-lg">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>{feature.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Categories Section */}
      <section className="bg-gray-50 rounded-lg p-8">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-800 mb-4">
            Categorías Populares
          </h2>
          <p className="text-gray-600">
            Encuentra el equipo que necesitas por categoría
          </p>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {categories.map((category, index) => (
            <Link 
              key={index}
              to={`/equipment?category=${encodeURIComponent(category)}`}
              className="bg-white p-4 rounded-lg text-center hover:shadow-md transition-shadow border"
            >
              <div className="text-orange-600 font-semibold">{category}</div>
            </Link>
          ))}
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-orange-600 text-white rounded-lg p-8">
        <div className="grid md:grid-cols-3 gap-8 text-center">
          <div>
            <div className="text-4xl font-bold mb-2">1000+</div>
            <div className="text-orange-100">Equipos Disponibles</div>
          </div>
          <div>
            <div className="text-4xl font-bold mb-2">500+</div>
            <div className="text-orange-100">Usuarios Activos</div>
          </div>
          <div>
            <div className="text-4xl font-bold mb-2">4.8</div>
            <div className="text-orange-100 flex items-center justify-center">
              <Star className="h-5 w-5 mr-1 fill-current" />
              Calificación Promedio
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="text-center py-16">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">
          ¿Listo para comenzar?
        </h2>
        <p className="text-gray-600 mb-8 max-w-2xl mx-auto">
          Únete a miles de usuarios que ya confían en ConstructMarket para sus necesidades de maquinaria
        </p>
        <Link to="/register">
          <Button size="lg" className="bg-orange-600 hover:bg-orange-700">
            Crear Cuenta Gratis
          </Button>
        </Link>
      </section>
    </div>
  )
}

export default Home

