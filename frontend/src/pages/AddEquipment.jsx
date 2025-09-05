import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Plus } from 'lucide-react'

const AddEquipment = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-800">Publicar Equipo</h1>
        <p className="text-gray-600">Agrega tu maquinaria al marketplace</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Plus className="h-5 w-5 mr-2" />
            Formulario de Publicación
          </CardTitle>
          <CardDescription>
            Esta funcionalidad está en desarrollo
          </CardDescription>
        </CardHeader>
        <CardContent className="text-center py-12">
          <Plus className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-800 mb-2">
            Próximamente
          </h3>
          <p className="text-gray-600 mb-4">
            El formulario para publicar equipos estará disponible pronto
          </p>
          <Button disabled>
            Publicar Equipo
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}

export default AddEquipment

