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
		'es' => 'Hola Mundo!',
		'de' => 'Hallo Welt!'
	),
	strtolower('Access Control') => array(
		'es' => 'Control de Acceso',
		'de' => 'Zugangskontrolle'
	),
	strtolower('User name') => array(
		'es' => 'Nombre de usuario',
		'de' => 'Benutzername'
	),
	strtolower('Login') => array(
		'es' => 'Ingresar',
		'de' => 'Einloggen'
	),
	strtolower('Sign In') => array(
		'es' => 'Ingresar',
		'de' => 'Anmelden'
	),
	strtolower('Password') => array(
		'es' => 'Contraseña',
		'de' => 'Kennwort'
	),
	strtolower('User is disabled. Contact the administrator') => array(
		'es' => 'El Usuario está desactivado. Contactar al administrador',
		'de' => 'Benutzer deaktiviert. Wenden Sie den Administrator an.'
	),
	strtolower('Invalid login') => array(
		'es' => 'Ingreso inválido',
		'de' => 'Ungültiger Anmeldeversuch'
	),

	strtolower('Toggle navigation') => array(
		'es' => 'Cambiar navegación',
		'de' => 'Navigation umschalten'
	),
	strtolower('Hello') => array(
		'es' => 'Hola',
		'de' => 'Hallo'
	),
	strtolower('Settings') => array(
		'es' => 'Configuración',
		'de' => 'Einstellungen'
	),
	strtolower('Help') => array(
		'es' => 'Ayuda',
		'de' => 'Hilfe'
	),
	strtolower('Log out') => array(
		'es' => 'Salir',
		'de' => 'Abmelden'
	),
	strtolower('Events') => array(
		'es' => 'Eventos',
		'de' => 'Veranstaltungen'
	),
	strtolower('Live') => array(
		'es' => 'En vivo',
		'de' => 'Live'
	),
	strtolower('Search') => array(
		'es' => 'Buscar',
		'de' => 'Suchen'
	),
	strtolower('Visitors') => array(
		'es' => 'Visitas',
		'de' => 'Besuch'
	),
	strtolower('Door Groups') => array(
		'es' => 'Grupos de Puertas',
		'es' => 'Türengruppe'
	),
	strtolower('Manage Visitors') => array(
		'es' => 'Administrar Visitas',
		'es' => 'Besuch verwalten'
	),
	strtolower('Organizations') => array(
		'es' => 'Organizaciones',
		'de' => 'Vereinigungen'
	),
	strtolower('Persons') => array(
		'es' => 'Personas',
		'de' => 'Personen'
	),
	strtolower('Controllers') => array(
		'es' => 'Controladores',
		'de' => 'Controllers'
	),
	strtolower('Zones') => array(
		'es' => 'Zonas',
		'de' => 'Zonen'
	),
	strtolower('Doors') => array(
		'es' => 'Puertas',
		'de' => 'Türen'
	),
	strtolower('Manage Doors') => array(
		'es' => 'Administrar Puertas',
		'de' => 'Türen verwalten'
	),
	strtolower('Accesses') => array(
		'es' => 'Accesos',
		'de' => 'Zugriffe'
	),
	strtolower('Person') => array(
		'es' => 'Persona',
		'de' => 'Person'
	),
	strtolower('Manage Persons') => array(
		'es' => 'Administrar Personas',
		'de' => 'Personen verwalten'
	),
	strtolower('Search Persons') => array(
		'es' => 'Buscar Personas',
		'de' => 'Personen suchen'
	),
	
	strtolower('Door') => array(
		'es' => 'Puerta',
		'de' => 'Tür'
	),
	strtolower('System Users') => array(
		'es' => 'Usuarios de sistema',
		'de' => 'Systembenutzer'
	),

	//events search
	strtolower('Event Search') => array(
		'es' => 'Búsqueda de Eventos',
		'de' => 'Veranstaltungen suchen'
	),
	strtolower('Filter options') => array(
		'es' => 'Filtrar opciones',
		'de' => 'Optionen auswählen'
	),
	strtolower('Zone') => array(
		'es' => 'Zona',
		'de' => 'Zone'
	),
	strtolower('Direction') => array(
		'es' => 'Dirección',
		'de' => 'Richtung'
	),
	strtolower('Both') => array(
		'es' => 'Ambos',
		'de' => 'beide'
	),
	strtolower('Incoming') => array(
		'es' => 'Entrante',
		'de' => 'ankommend'
	),
	strtolower('Outgoing') => array(
		'es' => 'Saliente',
		'de' => 'ausgehend'
	),
	strtolower('Date and Time') => array(
		'es' => 'Fecha y Hora',
		'de' => 'Datum und Uhr.'
	),
	strtolower('From') => array(
		'es' => 'Desde',
		'de' => 'von'
	),
	strtolower('From Date') => array(
		'es' => 'Desde Fecha',
		'de' => 'Seit Datum'
	),
	strtolower('Until') => array(
		'es' => 'Hasta',
		'de' => 'bis'
	),
	strtolower('Until Date') => array(
		'es' => 'Hasta Fecha',
		'de' => 'Bis Datum'
	),
	strtolower('Reset') => array(
		'es' => 'Resetear',
		'de' => 'Neu starten'
	),
	strtolower('Go back to search') => array(
		'es' => 'Volver a buscar',
		'de' => 'züruck nach suchen'
	),
	strtolower('Export spreadsheet') => array(
		'es' => 'Exportar hoja de datos',
		'de' => 'Tabellenkalkulation exportieren'
	),
	strtolower('Persons in gray were deleted or are visitors who left the building') => array(
		'es' => 'Las personas en gris fueron borradas o son visitas que dejaron el lugar',
		'de' => 'Graue Personen wären gelöscht oder sie sind Besucher, die das Gebäude schon verlässt haben'
	),
	strtolower('Event Type') => array(
		'es' => 'Tipo de Evento',
		'de' => 'Sortierung des Veranstaltung'
	),
	strtolower('Identified Access') => array(
		'es' => 'Acceso Identificado',
		'de' => 'Zugriff festgestellt'
	),
	strtolower('Access with button') => array(
		'es' => 'Acceso con botón',
		'de' => 'Mit Button zugriffen'
	),
	strtolower('Door remains opened') => array(
		'es' => 'Puerta permanece abierta',
		'de' => 'Tür bleibt geöffnet'
	),
	strtolower('Door was forced') => array(
		'es' => 'Puerta forzada',
		'de' => 'Die Tür war gewaltsam geöffnet'
	),
	strtolower('Card Reader') => array(
		'es' => 'Lector de tarjeta',
		'de' => 'Kartenleser'
	),
	strtolower('Fingerprint Reader') => array(
		'es' => 'Lector de huella',
		'de' => 'Fingerabdruckscanner'
	),
	strtolower('Button') => array(
		'es' => 'Botón',
		'de' => 'Button'
	),
	strtolower('Denial Cause') => array(
		'es' => 'Causa de negación',
		'de' => 'Versagungsgrund'
	),
	strtolower('No Access') => array(
		'es' => 'Sin Acceso',
		'de' => 'Kein Zugriff'
	),
	strtolower('Expired Card') => array(
		'es' => 'Tarjeta Expirada',
		'de' => 'Abgelaufene Karte'
	),
	strtolower('Out of time') => array(
		'es' => 'Fuera de tiempo',
		'de' => 'Aus der Zeit'
	),
	strtolower('Invalid value for') => array(
		'es' => 'Valor inválido para',
		'de' => 'ungültiger Wert für'
	),
	strtolower('Organization') => array(
		'es' => 'Organización',
		'de' => 'Organisation'
	),
	strtolower('Operation failed, please try again') => array(
		'es' => 'Operación fallida, intente nuevamente',
		'de' => 'Operation war gescheitert, bitte versuchen Sie es noch einmal'
	),
	strtolower('Type') => array(
		'es' => 'Tipo',
		'de' => 'Sortierung'
	),
	strtolower('Lock') => array(
		'es' => 'Cerradura',
		'de' => 'Schloss'
	),
	strtolower('Date') => array(
		'es' => 'Fecha',
		'de' => 'Datum'
	),
	strtolower('Time') => array(
		'es' => 'Hora',
		'de' => 'Uhr'
	),
	strtolower('Allowed') => array(
		'es' => 'Permitido',
		'de' => 'Erlaubt'
	),
	strtolower('No') => array(
		'es' => 'No',
		'de' => 'Nein'
	),
	strtolower('Yes') => array(
		'es' => 'Si',
		'de' => 'Ja'
	),
	strtolower('Paging navigation') => array(
		'es' => 'Navegación de paginado',
		'de' => 'Seiten surfen'
	),
	strtolower('Previous') => array(
		'es' => 'Anterior',
		'de' => 'vorige'
	),
	strtolower('Next') => array(
		'es' => 'Siguiente',
		'de' => 'nächste'
	),
	strtolower('Person Deleted') => array(
		'es' => 'Persona Borrada',
		'de' => 'Persone gelöscht'
	),
	strtolower('Total results') => array(
		'es' => 'Total de resultados',
		'de' => 'Total Ergebnise'
	),

	//events live
	strtolower('Reset filter') => array(
		'es' => 'Limpiar filtro',
		'de' => 'Filter neu starten'
	),
	strtolower('Clear events') => array(
		'es' => 'Limpiar eventos',
		'de' => 'Veranstaltungen löschen'
	),

	//events purge
	strtolower('Purge') => array(
		'es' => 'Purgar',
		'de' => 'reinigen'
	),
	strtolower('Events Purge') => array(
		'es' => 'Purgar Eventos',
		'de' => 'Veranstaltungen reinigen'
	),
	strtolower('Events before selected date and time will be erased') => array(
		'es' => 'Los eventos ocurridos antes de la fecha y hora indicados serán borrados',
		'de' => 'Die passierten Veranstaltungen vor angezeiten Datum und Uhr werden gelöscht'
	),
	strtolower('Purge Until') => array(
		'es' => 'Purgar Hasta',
		'de' => 'reinigen bis'
	),
	strtolower('Purge Until Time') => array(
		'es' => 'Purgar Hasta Hora',
		'de' => 'reinigen bis Uhr'
	),
	strtolower('Delete Events') => array(
		'es' => 'Eliminar Eventos',
		'de' => 'Veranstaltungen löschen'
	),
	strtolower('Are you sure you want to remove all events before') => array(
		'es' => 'Está seguro que quiere eliminar todos los eventos anteriores a',
		'de' => 'Sind Sie sicher, alle vorherigen Veranstaltungen löschen'
	),
	strtolower('events were deleted successfully') => array(
		'es' => 'eventos fueron eliminados exitosamente',
		'de' => 'Veranstaltungen würden erfolgreich gelöscht'
	),

	//events live
	strtolower('Events Live') => array(
		'es' => 'Eventos en Vivo',
		'de' => 'live Veranstaltungen'
	),
	strtolower('Filter') => array(
		'es' => 'Filtrar',
		'de' => 'filtern'
	),
	strtolower('No events') => array(
		'es' => 'Sin eventos',
		'de' => 'Keine Veranstaltungen'
	),

	//visit door groups
	strtolower('Groups') => array(
		'es' => 'Grupos',
		'de' => 'Gruppe'
	),
	strtolower('New') => array(
		'es' => 'Crear',
		'de' => 'Neu'
	),
	strtolower('Edit') => array(
		'es' => 'Editar',
		'de' => 'bearbeiten'
	),
	strtolower('Delete') => array(
		'es' => 'Borrar',
		'de' => 'löschen'
	),

	strtolower('New Door Group') => array(
		'es' => 'Crear Grupo de Puertas',
		'de' => 'Türengruppe erstellen'
	),
	strtolower('Door Group') => array(
		'es' => 'Grupo de Puertas',
		'de' => 'Türengruppe'
	),
	strtolower('Name') => array(
		'es' => 'Nombre',
		'de' => 'Name'
	),
	strtolower('Names') => array(
		'es' => 'Nombres',
		'de' => 'Namen'
	),
	strtolower('First Name') => array(
		'es' => 'Nombre de Pila',
		'de' => 'Vorname'
	),
	strtolower('Last Name') => array(
		'es' => 'Apellido',
		'de' => 'Nachname'
	),
	strtolower('Select all') => array(
		'es' => 'Seleccionar todos',
		'de' => 'Alles auswählen'
	),
	strtolower('Doors in the group') => array(
		'es' => 'Puertas en el grupo',
		'de' => 'Türen in die Gruppe'
	),
	strtolower('Are you sure') => array(
		'es' => 'Está seguro',
		'de' => 'Sind Sie sicher'
	),
	strtolower('Save') => array(
		'es' => 'Guardar',
		'de' => 'Speichern'
	),
	strtolower('Cancel') => array(
		'es' => 'Cancelar',
		'de' => 'Abbrechen'
	),
	strtolower('Edit Door Group') => array(
		'es' => 'Editar Grupo de Puertas',
		'de' => 'Türengruppe bearbeiten'
	),
	strtolower('For Visits') => array(
		'es' => 'Para Visitas',
		'de' => 'Besucher'
	),

	//visit manage visits
	strtolower('Manage Visitors') => array(
		'es' => 'Administrar Visitas',
		'de' => 'Besucher verwalten'
	),
	strtolower('Visiting Organization') => array(
		'es' => 'Visita a Organización',
		'de' => 'Vereinigung besuchen'
	),
	strtolower('Card Number') => array(
		'es' => 'Número de Tarjeta',
		'de' => 'Kartenummer'
	),
	strtolower('Add') => array(
		'es' => 'Agregar',
		'de' => 'hinzugügen'
	),
	strtolower('Remove') => array(
		'es' => 'Remover',
		'de' => 'entfernen'
	),
	strtolower('Add Visitor') => array(
		'es' => 'Agregar Visita',
		'de' => 'Besucher hinzufügen'
	),
	strtolower('Identification Number') => array(
		'es' => 'Número de Identificación',
		'de' => 'Kennnummer'
	),
	strtolower('Expiration') => array(
		'es' => 'Expiración',
		'de' => 'Ablauf'
	),
	strtolower('Expiration Date') => array(
		'es' => 'Fecha de Expiración',
		'de' => 'Gültigkeitsdatum'
	),
	strtolower('Expiration Hour') => array(
		'es' => 'Hora de Expiración',
		'de' => 'Gültigkeitsuhr'
	),
	strtolower('Visit Door Group') => array(
		'es' => 'Grupo de Puertas de Visitas',
		'de' => 'Besuchertürengruppe'
	),
	strtolower('Visit Door Groups') => array(
		'es' => 'Grupos de Puertas de Visitas',
		'de' => 'Besuchertürengruppen'
	),
	strtolower('Please fill the Visit Names field') => array(
		'es' => 'Por favor llenar el campo de Nombres de Visita',
		'de' => 'Bitte hinzufügen Sie die Bescuhername im Datenfeld'
	),
	strtolower('Please fill the Visit Last Name field') => array(
		'es' => 'Por favor llenar el campo de Apellido de Visita',
		'de' => 'Bitte hinzufügen Sie die Bescuhernachname im Datenfeld'
	),
	strtolower('Please fill the Identification Number field') => array(
		'es' => 'Por favor llenar el campo de Número de Identificación',
		'de' => 'Bitte hinzufügen Sie das Kennnummer im Datenfeld'
	),
	strtolower('Please fill the Card Number field') => array(
		'es' => 'Por favor llenar el campo de Número de Tarjeta',
		'de' => 'Bitte hinzufügen Sie das Kartenummer im Datenfeld'
	),
	strtolower('Please select an Organization') => array(
		'es' => 'Por favor seleccione una Organización',
		'de' => 'Bitte wählen Sie eine Vereinigung aus'
	),
	strtolower('Please select at least one Door Group') => array(
		'es' => 'Por favor seleccionar al menos un Grupo de Puertas',
		'de' => 'Bitte wählen Sie mindestens eine Türengruppe aus'
	),
	strtolower('Edit Visitor') => array(
		'es' => 'Editar Visita',
		'de' => 'Besucher bearbeiten'
	),
	strtolower('Invalid visit selected') => array(
		'es' => 'Visita seleccionada inválida',
		'de' => 'ausgewählte Bescuher unerkennbar'
	),

	//organizations
	strtolower('New Organization') => array(
		'es' => 'Nueva Organización',
		'de' => 'Neue Vereinigung'
	),
	strtolower('Edit Organization') => array(
		'es' => 'Editar Organización',
		'de' => 'Vereinigung bearbeiten'
	),
	strtolower('Deleting this organization will remove all persons that belongs to it') => array(
		'es' => 'Borrar esta organización va a remover a todas las personas que pertenecen a la misma',
		'de' => 'Durch das Löschen dieser Organisation werden alle dazugehörigen Personen entfernt'
	),

	//persons
	strtolower('New Person') => array(
		'es' => 'Nueva Persona',
		'de' => 'Neue Person'
	),
	strtolower('Edit Person') => array(
		'es' => 'Editar Persona',
		'de' => 'Person bearbeiten'
	),
	strtolower('Import CSV') => array(
		'es' => 'Importar CSV',
		'de' => 'CSV importieren'
	),
	strtolower('Import a .CSV file with rows with the following format') => array(
		'es' => 'Importar un archivo .CSV de filas con el siguiente formato',
		'de' => 'eine CSV-Datei aus Zeilen mit dem folgenden Format importieren'
	),
	strtolower('Ignore first line of file (column headers)') => array(
		'es' => 'Ignorar primer línea de archivo (encabezados de columna)',
		'de' => 'Erste Dateizeile ignorieren (Spaltenüberschriften)'
	),
	strtolower('Send') => array(
		'es' => 'Enviar',
		'de' => 'senden'
	),
	strtolower('Make sure the csv file has the correct format, and preferably UTF-8 encoding.') => array(
		'es' => 'Asegurese que el archivo CSV tenga un formato correcto, preferiblemente con encoding UTF-8.',
		'de' => 'Stellen Sie sicher, dass die CSV-Datei ein korrektes Format hat, vorzugsweise mit UTF-8-Codierung.'
	),
	strtolower('Total persons imported') => array(
		'es' => 'Total de personas importadas',
		'de' => 'insgesamt importierte Personen'
	),
	strtolower('Refresh') => array(
		'es' => 'Refrescar',
		'de' => 'aktualisieren'
	),
	strtolower('Note') => array(
		'es' => 'Nota',
		'de' => 'Vermerk'
	),
	strtolower('Export') => array(
		'es' => 'Exportar',
		'de' => 'exportieren'
	),
	strtolower('Export persons to Excel') => array(
		'es' => 'Exportar personas a Excel',
		'de' => 'Personen nach Excel exportieren'
	),

	//controllers
	strtolower('Controllers') => array(
		'es' => 'Controladores',
		'de' => 'Treibers'
	),
	strtolower('Filter names') => array(
		'es' => 'Filtrar nombres',
		'de' => 'Namen filtern'
	),
	strtolower('Controller Model') => array(
		'es' => 'Modelo de Controlador',
		'de' => 'Treibermodell'
	),
	strtolower('Reprogram') => array(
		'es' => 'Reprogramar',
		'de' => 'neu programmieren'
	),
	strtolower('New Controller') => array(
		'es' => 'Nuevo Controlador',
		'de' => 'Neuer Treiber'
	),
	strtolower('MAC Address') => array(
		'es' => 'Dirección MAC',
		'de' => 'MAC Adresse'
	),
	strtolower('Are you sure you want to reprogram this controller') => array(
		'es' => 'Está seguro que quiere reprogramar este controlador',
		'de' => 'Sind Sie sicher, dieser Treiber neu programmieren'
	),
	strtolower('Power Off') => array(
		'es' => 'Apagar',
		'de' => 'Herunterfahren'
	),
	strtolower('Are you sure you want to power off this controller') => array(
		'es' => 'Está seguro que quiere apagar este controlador',
		'de' => 'Sind Sie sicher, dieser Treiber herunterfahren'
	),
	strtolower('Last Seen') => array(
		'es' => 'Visto Últ.',
		'de' => 'zuletzt gesehen'
	),
	strtolower('Reachable') => array(
		'es' => 'Accesible',
		'de' => 'Zugänglich'
	),
	strtolower('MAC address sent is not valid') => array(
		'es' => 'Dirección MAC enviada inválida',
		'de' => 'Ungültige MAC-Adresse'
	),
	strtolower('Invalid values sent') => array(
		'es' => 'Valores enviados inválidos',
		'de' => 'Ungültige gesendete Werte'
	),
	strtolower('IP Address') => array(
		'es' => 'Dirección IP',
		'de' => 'IP Adresse'
	),

	//zones
	strtolower('New Zone') => array(
		'es' => 'Nueva Zona',
		'de' => 'Neue Zone'
	),
	strtolower('Edit Zone') => array(
		'es' => 'Editar Zona',
		'de' => 'Zone bearbeiten'
	),
	strtolower('Deleting this zone will remove all doors that belongs to it') => array(
		'es' => 'Borrar esta zona va a remover todas las puertas que pertenecen a la misma',
		'de' => 'Durch Löschen dieses Bereichs werden alle dazugehörigen Türen entfernt.'
	),

	//doors
	strtolower('Door Number') => array(
		'es' => 'Número de Puerta',
		'de' => 'Türnummer'
	),
	strtolower('None') => array(
		'es' => 'Ninguno',
		'de' => 'Keine'
	),
	strtolower('Visit Exit') => array(
		'es' => 'Salida de Visita',
		'de' => 'Besucher ausgang'
	),
	strtolower('Times') => array(
		'es' => 'Tiempos',
		'de' => 'Zeiten'
	),
	strtolower('Release Time (s)') => array(
		'es' => 'T. de Apertura (s)',
		'de' => 'Öffnungszeit (en)'
	),
	strtolower('Buzzer Time (s)') => array(
		'es' => 'T. de Buzzer (s)',
		'de' => 'Summer Zeit (en)'
	),
	strtolower('Alarm Timeout (s)') => array(
		'es' => 'T. de Alarma (s)',
		'de' => 'Alarm Zeit (en)'
	),
	strtolower('Door Sensor') => array(
		'es' => 'Sensor de Puerta',
		'de' => 'Türsensor'
	),
	strtolower('NC (Normally Closed)') => array(
		'es' => 'NC (Normal Cerrado)',
		'de' => 'NC (Normaleweise geschlossen)'
	),
	strtolower('NO (Normally Open)') => array(
		'es' => 'NO (Normal Abierto)',
		'de' => 'NO (Normaleweise geöffnet)'
	),
	strtolower('Deleting this door will remove all events that belong to it') => array(
		'es' => 'Borrar esta puerta va a remover todos los eventos que pertenecen a la misma',
		'de' => 'Durch Löschen dieser Tür werden alle dazugehörigen Ereignisse entfernt.'
	),
	strtolower('New Door') => array(
		'es' => 'Nueva Puerta',
		'de' => 'Neue Tür'
	),
	strtolower('Edit Door') => array(
		'es' => 'Editar Puerta',
		'de' => 'Tür bearbeiten'
	),

	//accesses
	strtolower('Access: Person') => array(
		'es' => 'Accesos: Persona',
		'de' => 'Zugriffe: Person'
	),
	strtolower('Add to all') => array(
		'es' => 'Agregar a todos',
		'de' => 'Alle hinzufügen'
	),
	strtolower('All Week') => array(
		'es' => 'Semana Compl.',
		'de' => 'Ganze Woche'
	),
	strtolower('Make sure to select at least 1 row') => array(
		'es' => 'Seleccionar al menos 1 fila',
		'de' => 'Mindestens eine Zeile auswählen'
	),
	strtolower('Schedule') => array(
		'es' => 'Calendario',
		'de' => 'Kalender'
	),
	strtolower('Day') => array(
		'es' => 'Día',
		'de' => 'Tag'
	),
	strtolower('Time interval') => array(
		'es' => 'Intervalo de Tiempo',
		'de' => 'Zeitintervall'
	),
	strtolower('Incoming') => array(
		'es' => 'Entrante',
		'de' => 'Eingang'
	),
	strtolower('Outgoing') => array(
		'es' => 'Saliente',
		'de' => 'Ausgang'
	),
	strtolower('Both') => array(
		'es' => 'Ambos',
		'de' => 'Beide'
	),
	strtolower('Every day') => array(
		'es' => 'Todos los días',
		'de' => 'Täglich'
	),
	strtolower('Monday') => array(
		'es' => 'Lunes',
		'de' => 'Montag'
	),
	strtolower('Tuesday') => array(
		'es' => 'Martes',
		'de' => 'Dienstag'
	),
	strtolower('Wednesday') => array(
		'es' => 'Miércoles',
		'de' => 'Mittwoch'
	),
	strtolower('Thursday') => array(
		'es' => 'Jueves',
		'de' => 'Donnerstag'
	),
	strtolower('Friday') => array(
		'es' => 'Viernes',
		'de' => 'Freitag'
	),
	strtolower('Saturday') => array(
		'es' => 'Sábado',
		'de' => 'Samstag'
	),
	strtolower('Sunday') => array(
		'es' => 'Domingo',
		'de' => 'Sonntag'
	),
	strtolower('New access for') => array(
		'es' => 'Nuevo acceso para',
		'de' => 'Neue Zugriff für'
	),
	strtolower('Editing') => array(
		'es' => 'Editando',
		'de' => 'Wird bearbeitet'
	),
	strtolower('Error fetching access data') => array(
		'es' => 'Error obteniendo información del acceso',
		'de' => 'Fehler beim Abrufen der Zugriffsinformationen'
	),
	strtolower('You must select at least 1 day of the week or check \'Every day\'') => array(
		'es' => 'Debe seleccionar al menos 1 día de la semana o marcar \'Todos los días\'',
		'de' => 'Sie müssen mindestens einen Wochentag auswählen oder \'Täglich\' aktivieren.'
	),
	strtolower('Error when trying to create access') => array(
		'de' => 'Fehler beim Erstellen des Zugriffs',
	),
	strtolower('Error when trying to edit access') => array(
		'es' => 'Error al intentar editar acceso',
		'de' => 'Fehler beim Bearbeiten des Zugriffs'
	),
	strtolower('Access: Door') => array(
		'es' => 'Accesos: Puerta',
		'de' => 'Zugriffe: Tür'
	),
	strtolower('Create access to') => array(
		'es' => 'Crear acceso para',
		'de' => 'Zügrif erstellen für'
	),

	//system users
	strtolower('New System User') => array(
		'es' => 'Nuevo Usuario de Sistema',
		'de' => 'Neue Systembenutzer'
	),
	strtolower('Full Name') => array(
		'es' => 'Nombre Completo',
		'de' => 'Vollständiger Name'
	),
	strtolower('Confirm Password') => array(
		'es' => 'Confirmar Contraseña',
		'de' => 'Kennwort bestätigen'
	),
	strtolower('Role') => array(
		'es' => 'Rol',
		'de' => 'Stellung'
	),
	strtolower('Active') => array(
		'es' => 'Activo',
		'de' => 'Aktiv'
	),
	strtolower('Description') => array(
		'es' => 'Descripción',
		'de' => 'Beschreibung'
	),
	strtolower('Edit User') => array(
		'es' => 'Editar Usuario',
		'de' => 'Benutzer bearbeiten'
	),
	strtolower('Password and confirmation don\'t match') => array(
		'es' => 'Contraseña y confirmación no coinciden',
		'es' => 'Kennwort und Bestätigung stimmen nicht überein'
	),
	strtolower('Invalid role sent') => array(
		'es' => 'Rol enviado inválido',
		'de' => 'Ungültige gesendete Stellung'
	),
	strtolower('Admin user cannot be deleted') => array(
		'es' => 'Usuario Admin no puede ser borrado',
		'de' => 'Administrator kann nicht gelöscht werden'
	),
	strtolower('Please fill the field: Full name') => array(
		'es' => 'Llenar el campo de: Nombre Completo',
		'de' => 'Füllen Sie das Feld aus: Vollständiger Name'
	),
	strtolower('Settings saved') => array(
		'es' => 'Configuración guardada',
		'de' => 'Einstellungen gespeichert'
	),
	strtolower('Could not get user information') => array(
		'es' => 'No se pudo obtener información de usuario',
		'de' => 'Benutzerinformationen konnten nicht abgerufen werden'
	),
	strtolower('Language') => array(
		'es' => 'Idioma',
		'de' => 'Sprache'
	),
	strtolower('Language sent is not supported') => array(
		'es' => 'Idioma enviado no es soportado',
		'de' => 'Sprache wird nicht unterstützt'
	),
	strtolower('Viewer') => array(
		'es' => 'Visualizador',
		'de' => 'Dateiviewer'
	),
	strtolower('Operator') => array(
		'es' => 'Operador',
		'de' => 'Operator'
	),
	strtolower('Administrator') => array(
		'es' => 'Administrador',
		'de' => 'Administrator'
	),
	
	//Search Person
	strtolower('Last Name Pattern') => array(
		'es' => 'Patrón Búsqueda de Apellido',
		'de' => 'Nachname Suchmuster'
	),
	strtolower('Names Pattern') => array(
		'es' => 'Patrón Búsqueda de Nombre',
		'de' => 'Vorname Suchmuster'
	),
	strtolower('Please fill at least one field') => array(
		'es' => 'Favor de llenar al menos un campo',
		'de' => 'Bitte füllen Sie mindestens ein Feld aus'
	),
	strtolower('Ident. #') => array(
		'es' => '# de Ident.',
		'de' => 'Identifikationnummer'
	),
	strtolower('Card #') => array(
		'es' => '# de Tarjeta',
		'de' => 'Kartenummer'
	),
	strtolower('No results') => array(
		'es' => 'Sin resultados',
		'de' => 'Keine Ergebnisse'
	)
);

?>