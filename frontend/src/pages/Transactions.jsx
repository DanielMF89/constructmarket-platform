import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { FileText } from 'lucide-react'

const Transactions = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-800">Mis Transacciones</h1>
        <p className="text-gray-600">Historial de compras, ventas y rentas</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <FileText className="h-5 w-5 mr-2" />
            Historial de Transacciones
          </CardTitle>
          <CardDescription>
            Esta funcionalidad está en desarrollo
          </CardDescription>
        </CardHeader>
        <CardContent className="text-center py-12">
          <FileText className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-800 mb-2">
            Sin transacciones
          </h3>
          <p className="text-gray-600">
            Aquí aparecerán tus compras, ventas y rentas
          </p>
        </CardContent>
      </Card>
    </div>
  )
}

export default Transactions

