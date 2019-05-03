<?php
$dictionary = array();

//get translations of a text
//usage: get_text("Settings", "es");
function get_text($token, $lang = null){
    global $dictionary;
    if (empty($lang)
        || !array_key_exists(strtolower($token), $dictionary)
        || !array_key_exists($lang, $dictionary[strtolower($token)])
    ) {
        return $token;
    } else {
        return $dictionary[strtolower($token)][$lang];
    }
}

//$dictionary[strtolower('Hello World!')] = array('fr' => 'Bonjour tout le monde!','de' => 'Hallo Welt!');
$dictionary = array(
	strtolower('Hello world!') => array(
		'es' => 'Hola Mundo!'
	),
	strtolower('Access Control') => array(
		'es' => 'Control de Acceso'
	),
	strtolower('User name') => array(
		'es' => 'Nombre de usuario'
	),
	strtolower('Login') => array(
		'es' => 'Ingresar'
	),
	strtolower('Sign In') => array(
		'es' => 'Ingresar'
	),
	strtolower('Password') => array(
		'es' => 'Contraseña'
	),
	strtolower('User is disabled. Contact the administrator') => array(
		'es' => 'El Usuario está desactivado. Contactar al administrador'
	),
	strtolower('Invalid login') => array(
		'es' => 'Ingreso inválido'
	),

	strtolower('Toggle navigation') => array(
		'es' => 'Cambiar navegación'
	),
	strtolower('Hello') => array(
		'es' => 'Hola'
	),
	strtolower('Settings') => array(
		'es' => 'Configuración'
	),
	strtolower('Help') => array(
		'es' => 'Ayuda'
	),
	strtolower('Log out') => array(
		'es' => 'Salir'
	),
	strtolower('Events') => array(
		'es' => 'Eventos'
	),
	strtolower('Live') => array(
		'es' => 'En vivo'
	),
	strtolower('Search') => array(
		'es' => 'Buscar'
	),
	strtolower('Visitors') => array(
		'es' => 'Visitas'
	),
	strtolower('Visit Door Groups') => array(
		'es' => 'Grupos de Puertas de Visitas'
	),
	strtolower('Manage Visitors') => array(
		'es' => 'Administrar Visitas'
	),
	strtolower('Organizations') => array(
		'es' => 'Organizaciones'
	),
	strtolower('Persons') => array(
		'es' => 'Personas'
	),
	strtolower('Controllers') => array(
		'es' => 'Controladores'
	),
	strtolower('Zones') => array(
		'es' => 'Zonas'
	),
	strtolower('Doors') => array(
		'es' => 'Puertas'
	),
	strtolower('Accesses') => array(
		'es' => 'Accesos'
	),
	strtolower('Person') => array(
		'es' => 'Persona'
	),
	strtolower('Manage Persons') => array(
		'es' => 'Administrar Personas'
	),
	strtolower('Search Persons') => array(
		'es' => 'Buscar Personas'
	),
	
	strtolower('Door') => array(
		'es' => 'Puerta'
	),
	strtolower('System Users') => array(
		'es' => 'Usuarios de sistema'
	),

	//events search
	strtolower('Event Search') => array(
		'es' => 'Búsqueda de Eventos'
	),
	strtolower('Filter options') => array(
		'es' => 'Filtrar opciones'
	),
	strtolower('Zone') => array(
		'es' => 'Zona'
	),
	strtolower('Direction') => array(
		'es' => 'Dirección'
	),
	strtolower('Both') => array(
		'es' => 'Ambos'
	),
	strtolower('Incoming') => array(
		'es' => 'Entrante'
	),
	strtolower('Outgoing') => array(
		'es' => 'Saliente'
	),
	strtolower('Date and Time') => array(
		'es' => 'Fecha y Hora'
	),
	strtolower('From') => array(
		'es' => 'Desde'
	),
	strtolower('From Date') => array(
		'es' => 'Desde Fecha'
	),
	strtolower('Until') => array(
		'es' => 'Hasta'
	),
	strtolower('Until Date') => array(
		'es' => 'Hasta Fecha'
	),
	strtolower('Reset') => array(
		'es' => 'Resetear'
	),
	strtolower('Go back to search') => array(
		'es' => 'Volver a buscar'
	),
	strtolower('Export spreadsheet') => array(
		'es' => 'Exportar hoja de datos'
	),
	strtolower('Persons in gray were deleted or are visitors who left the building') => array(
		'es' => 'Las personas en gris fueron borradas o son visitas que dejaron el lugar'
	),
	strtolower('Event Type') => array(
		'es' => 'Tipo de Evento'
	),
	strtolower('Identified Access') => array(
		'es' => 'Acceso Identificado'
	),
	strtolower('Access with button') => array(
		'es' => 'Acceso con botón'
	),
	strtolower('Door remains opened') => array(
		'es' => 'Puerta permanece abierta'
	),
	strtolower('Door was forced') => array(
		'es' => 'Puerta forzada'
	),
	strtolower('Card Reader') => array(
		'es' => 'Lector de tarjeta'
	),
	strtolower('Fingerprint Reader') => array(
		'es' => 'Lector de huella'
	),
	strtolower('Button') => array(
		'es' => 'Botón'
	),
	strtolower('Denial Cause') => array(
		'es' => 'Causa de negación'
	),
	strtolower('No Access') => array(
		'es' => 'Sin Acceso'
	),
	strtolower('Expired Card') => array(
		'es' => 'Tarjeta Expirada'
	),
	strtolower('Out of time') => array(
		'es' => 'Fuera de tiempo'
	),
	strtolower('Invalid value for') => array(
		'es' => 'Valor inválido para'
	),
	strtolower('Organization') => array(
		'es' => 'Organización'
	),
	strtolower('Operation failed, please try again') => array(
		'es' => 'Operación fallida, intente nuevamente'
	),
	strtolower('Type') => array(
		'es' => 'Tipo'
	),
	strtolower('Lock') => array(
		'es' => 'Cerradura'
	),
	strtolower('Date') => array(
		'es' => 'Fecha'
	),
	strtolower('Time') => array(
		'es' => 'Hora'
	),
	strtolower('Allowed') => array(
		'es' => 'Permitido'
	),
	strtolower('No') => array(
		'es' => 'No'
	),
	strtolower('Yes') => array(
		'es' => 'Si'
	),
	strtolower('Paging navigation') => array(
		'es' => 'Navegación de paginado'
	),
	strtolower('Previous') => array(
		'es' => 'Anterior'
	),
	strtolower('Next') => array(
		'es' => 'Siguiente'
	),
	strtolower('Person Deleted') => array(
		'es' => 'Persona Borrada'
	),

	//events live
	strtolower('Reset filter') => array(
		'es' => 'Limpiar filtro'
	),
	strtolower('Clear events') => array(
		'es' => 'Limpiar eventos'
	),

	//events purge
	strtolower('Purge') => array(
		'es' => 'Purgar'
	),
	strtolower('Events Purge') => array(
		'es' => 'Purgar Eventos'
	),
	strtolower('Events before selected date and time will be erased') => array(
		'es' => 'Los eventos ocurridos antes de la fecha y hora indicados serán borrados'
	),
	strtolower('Purge Until') => array(
		'es' => 'Purgar Hasta'
	),
	strtolower('Purge Until Time') => array(
		'es' => 'Purgar Hasta Hora'
	),
	strtolower('Delete Events') => array(
		'es' => 'Eliminar Eventos'
	),
	strtolower('Are you sure you want to remove all events before') => array(
		'es' => 'Está seguro que quiere eliminar todos los eventos anteriores a'
	),
	strtolower('events were deleted successfully') => array(
		'es' => 'eventos fueron eliminados exitosamente'
	),

	//events live
	strtolower('Events Live') => array(
		'es' => 'Eventos en Vivo'
	),
	strtolower('Filter') => array(
		'es' => 'Filtrar'
	),
	strtolower('No events') => array(
		'es' => 'Sin eventos'
	),

	//visit door groups
	strtolower('Groups') => array(
		'es' => 'Grupos'
	),
	strtolower('New') => array(
		'es' => 'Crear'
	),
	strtolower('Edit') => array(
		'es' => 'Editar'
	),
	strtolower('Delete') => array(
		'es' => 'Borrar'
	),
	strtolower('New Visitor Group') => array(
		'es' => 'Crear Grupo de Visitas'
	),
	strtolower('Name') => array(
		'es' => 'Nombre'
	),
	strtolower('Names') => array(
		'es' => 'Nombres'
	),
	strtolower('First Name') => array(
		'es' => 'Nombre de Pila'
	),
	strtolower('Last Name') => array(
		'es' => 'Apellido'
	),
	strtolower('Select all') => array(
		'es' => 'Seleccionar todos'
	),
	strtolower('Doors in the group') => array(
		'es' => 'Puertas en el grupo'
	),
	strtolower('Are you sure') => array(
		'es' => 'Está seguro'
	),
	strtolower('Save') => array(
		'es' => 'Guardar'
	),
	strtolower('Cancel') => array(
		'es' => 'Cancelar'
	),
	strtolower('Edit Visitor Group') => array(
		'es' => 'Editar Grupo de Visitas'
	),

	//visit manage visits
	strtolower('Manage Visitors') => array(
		'es' => 'Administrar Visitas'
	),
	strtolower('Visiting Organization') => array(
		'es' => 'Visita a Organización'
	),
	strtolower('Card Number') => array(
		'es' => 'Número de Tarjeta'
	),
	strtolower('Add') => array(
		'es' => 'Agregar'
	),
	strtolower('Remove') => array(
		'es' => 'Remover'
	),
	strtolower('Add Visitor') => array(
		'es' => 'Agregar Visita'
	),
	strtolower('Identification Number') => array(
		'es' => 'Número de Identificación'
	),
	strtolower('Expiration') => array(
		'es' => 'Expiración'
	),
	strtolower('Expiration Date') => array(
		'es' => 'Fecha de Expiración'
	),
	strtolower('Expiration Hour') => array(
		'es' => 'Hora de Expiración'
	),
	strtolower('Visit Door Group') => array(
		'es' => 'Grupo de Puertas de Visitas'
	),
	strtolower('Please fill the Visit Names field') => array(
		'es' => 'Por favor llenar el campo de Nombres de Visita'
	),
	strtolower('Please fill the Visit Last Name field') => array(
		'es' => 'Por favor llenar el campo de Apellido de Visita'
	),
	strtolower('Please fill the Identification Number field') => array(
		'es' => 'Por favor llenar el campo de Número de Identificación'
	),
	strtolower('Please fill the Card Number field') => array(
		'es' => 'Por favor llenar el campo de Número de Tarjeta'
	),
	strtolower('Please select an Organization') => array(
		'es' => 'Por favor seleccione una Organización'
	),
	strtolower('Please select at least one Door Group') => array(
		'es' => 'Por favor seleccionar al menos un Grupo de Puertas'
	),
	strtolower('Edit Visitor') => array(
		'es' => 'Editar Visita'
	),
	strtolower('Invalid visit selected') => array(
		'es' => 'Visita seleccionada inválida'
	),

	//organizations
	strtolower('New Organization') => array(
		'es' => 'Nueva Organización'
	),
	strtolower('Edit Organization') => array(
		'es' => 'Editar Organización'
	),
	strtolower('Deleting this organization will remove all persons that belongs to it') => array(
		'es' => 'Borrar esta organización va a remover a todas las personas que pertenecen a la misma'
	),

	//persons
	strtolower('New Person') => array(
		'es' => 'Nueva Persona'
	),
	strtolower('Edit Person') => array(
		'es' => 'Editar Persona'
	),
	strtolower('Import CSV') => array(
		'es' => 'Importar CSV'
	),
	strtolower('Import a .CSV file with rows with the following format') => array(
		'es' => 'Importar un archivo .CSV de filas con el siguiente formato'
	),
	strtolower('Ignore first line of file (column headers)') => array(
		'es' => 'Ignorar primer línea de archivo (encabezados de columna)'
	),
	strtolower('Send') => array(
		'es' => 'Enviar'
	),
	strtolower('Make sure the csv file has the correct format, and preferably UTF-8 encoding.') => array(
		'es' => 'Asegurese que el archivo CSV tenga un formato correcto, preferiblemente con encoding UTF-8.'
	),
	strtolower('Total persons imported') => array(
		'es' => 'Total de personas importadas'
	),
	strtolower('Refresh') => array(
		'es' => 'Refrescar'
	),
	strtolower('Note') => array(
		'es' => 'Nota'
	),

	//controllers
	strtolower('Controllers') => array(
		'es' => 'Controladores'
	),
	strtolower('Filter names') => array(
		'es' => 'Filtrar nombres'
	),
	strtolower('Controller Model') => array(
		'es' => 'Modelo de Controlador'
	),
	strtolower('Reprogram') => array(
		'es' => 'Reprogramar'
	),
	strtolower('New Controller') => array(
		'es' => 'Nuevo Controlador'
	),
	strtolower('MAC Address') => array(
		'es' => 'Dirección MAC'
	),
	strtolower('Are you sure you want to reprogram this controller') => array(
		'es' => 'Está seguro que quiere reprogramar este controlador'
	),
	strtolower('Power Off') => array(
		'es' => 'Apagar'
	),
	strtolower('Are you sure you want to power off this controller') => array(
		'es' => 'Está seguro que quiere apagar este controlador'
	),
	strtolower('Last Seen') => array(
		'es' => 'Visto Últ.'
	),
	strtolower('Reachable') => array(
		'es' => 'Accesible'
	),
	strtolower('MAC address sent is not valid') => array(
		'es' => 'Dirección MAC enviada inválida'
	),
	strtolower('Invalid values sent') => array(
		'es' => 'Valores enviados inválidos'
	),

	//zones
	strtolower('New Zone') => array(
		'es' => 'Nueva Zona'
	),
	strtolower('Edit Zone') => array(
		'es' => 'Editar Zona'
	),
	strtolower('Deleting this zone will remove all doors that belongs to it') => array(
		'es' => 'Borrar esta zona va a remover todas las puertas que pertenecen a la misma'
	),

	//doors
	strtolower('Door Number') => array(
		'es' => 'Número de Puerta'
	),
	strtolower('None') => array(
		'es' => 'Ninguno'
	),
	strtolower('Visit Exit') => array(
		'es' => 'Salida de Visita'
	),
	strtolower('Times') => array(
		'es' => 'Tiempos'
	),
	strtolower('Release Time (s)') => array(
		'es' => 'T. de Apertura (s)'
	),
	strtolower('Buzzer Time (s)') => array(
		'es' => 'T. de Buzzer (s)'
	),
	strtolower('Alarm Timeout (s)') => array(
		'es' => 'T. de Alarma (s)'
	),
	strtolower('Door Sensor') => array(
		'es' => 'Sensor de Puerta'
	),
	strtolower('NC (Normally Closed)') => array(
		'es' => 'NC (Normal Cerrado)'
	),
	strtolower('NO (Normally Open)') => array(
		'es' => 'NO (Normal Abierto)'
	),
	strtolower('Deleting this door will remove all events that belong to it') => array(
		'es' => 'Borrar esta puerta va a remover todos los eventos que pertenecen a la misma'
	),
	strtolower('New Door') => array(
		'es' => 'Nueva Puerta'
	),
	strtolower('Edit Door') => array(
		'es' => 'Editar Puerta'
	),

	//accesses
	strtolower('Access: Person') => array(
		'es' => 'Accesos: Persona'
	),
	strtolower('Add to all') => array(
		'es' => 'Agregar a todos'
	),
	strtolower('All Week') => array(
		'es' => 'Semana Compl.'
	),
	strtolower('Make sure to select at least 1 row') => array(
		'es' => 'Seleccionar al menos 1 fila'
	),
	strtolower('Schedule') => array(
		'es' => 'Calendario'
	),
	strtolower('Day') => array(
		'es' => 'Día'
	),
	strtolower('Time interval') => array(
		'es' => 'Intervalo de Tiempo'
	),
	strtolower('Incoming') => array(
		'es' => 'Entrante'
	),
	strtolower('Outgoing') => array(
		'es' => 'Saliente'
	),
	strtolower('Both') => array(
		'es' => 'Ambos'
	),
	strtolower('Every day') => array(
		'es' => 'Todos los días'
	),
	strtolower('Monday') => array(
		'es' => 'Lunes'
	),
	strtolower('Tuesday') => array(
		'es' => 'Martes'
	),
	strtolower('Wednesday') => array(
		'es' => 'Miércoles'
	),
	strtolower('Thursday') => array(
		'es' => 'Jueves'
	),
	strtolower('Friday') => array(
		'es' => 'Viernes'
	),
	strtolower('Saturday') => array(
		'es' => 'Sábado'
	),
	strtolower('Sunday') => array(
		'es' => 'Domingo'
	),
	strtolower('New access for') => array(
		'es' => 'Nuevo acceso para'
	),
	strtolower('Editing') => array(
		'es' => 'Editando'
	),
	strtolower('Error fetching access data') => array(
		'es' => 'Error obteniendo información del acceso'
	),
	strtolower('You must select at least 1 day of the week or check \'Every day\'') => array(
		'es' => 'Debe seleccionar al menos 1 día de la semana o marcar \'Todos los días\''
	),
	strtolower('Error when trying to create access') => array(
		'es' => 'Error al intentar crear acceso'
	),
	strtolower('Error when trying to edit access') => array(
		'es' => 'Error al intentar editar acceso'
	),
	strtolower('Access: Door') => array(
		'es' => 'Accesos: Puerta'
	),

	//system users
	strtolower('New System User') => array(
		'es' => 'Nuevo Usuario de Sistema'
	),
	strtolower('Full Name') => array(
		'es' => 'Nombre Completo'
	),
	strtolower('Confirm Password') => array(
		'es' => 'Confirmar Contraseña'
	),
	strtolower('Role') => array(
		'es' => 'Rol'
	),
	strtolower('Active') => array(
		'es' => 'Activo'
	),
	strtolower('Description') => array(
		'es' => 'Descripción'
	),
	strtolower('Edit User') => array(
		'es' => 'Editar Usuario'
	),
	strtolower('Password and confirmation don\'t match') => array(
		'es' => 'Contraseña y confirmación no coinciden'
	),
	strtolower('Invalid role sent') => array(
		'es' => 'Rol enviado inválido'
	),
	strtolower('Admin user cannot be deleted') => array(
		'es' => 'Usuario Admin no puede ser borrado'
	),
	strtolower('Please fill the field: Full name') => array(
		'es' => 'Llenar el campo de: Nombre Completo'
	),
	strtolower('Settings saved') => array(
		'es' => 'Configuración guardada'
	),
	strtolower('Could not get user information') => array(
		'es' => 'No se pudo obtener información de usuario'
	),
	strtolower('Language') => array(
		'es' => 'Idioma'
	),
	strtolower('Language sent is not supported') => array(
		'es' => 'Idioma enviado no es soportado'
	),
	strtolower('Viewer') => array(
		'es' => 'Visualizador'
	),
	strtolower('Operator') => array(
		'es' => 'Operador'
	),
	strtolower('Administrator') => array(
		'es' => 'Administrador'
	),
	
	//Search Person
	strtolower('Last Name Pattern') => array(
		'es' => 'Patrón Búsqueda de Apellido'
	),
	strtolower('Names Pattern') => array(
		'es' => 'Patrón Búsqueda de Nombre'
	),
	strtolower('Please fill at least one field') => array(
		'es' => 'Favor de llenar al menos un campo'
	),
	strtolower('Ident. #') => array(
		'es' => '# de Ident.'
	),
	strtolower('Card #') => array(
		'es' => '# de Tarjeta'
	),
	strtolower('No results') => array(
		'es' => 'Sin resultados'
	)
);

?>