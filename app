

Create
  request
    OK POST
  response
     OK BAD REQUEST 400  If the shitty ID
     OK NOT FOUND   404  If ID not exists
     OK OK          200  If the resource was updated

Retrieve
  request
    OK GET All
  response
    NOT FOUND
    OK

  request
    OK GET Single OK

  response
    NOT FOUND
    OK

Update
  request PUT OK
  response

Delete
  request DELETE OK
  response