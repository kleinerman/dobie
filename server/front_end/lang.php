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
	strtolower('Persons in red were deleted or they are visitors that left the building') => array(
		'es' => 'Las personas en rojo fueron borradas o son visitas que dejaron el lugar'
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
	strtolower('Please fill the Visit Name field') => array(
		'es' => 'Por favor llenar el campo de Nombre de Visita'
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
		'es' => 'Tiempo de Apertura (s)'
	),
	strtolower('Buzzer Time (s)') => array(
		'es' => 'Tiempo de Buzzer (s)'
	),
	strtolower('Alarm Timeout (s)') => array(
		'es' => 'Tiempo de Alarma (s)'
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
	strtolower('Access - Person -> Door') => array(
		'es' => 'Accesos - Persona -> Puerta'
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
	strtolower('Access - Door -> Person') => array(
		'es' => 'Accesos - Puerta -> Persona'
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
	)
);

?>