insert into bodegas (id, nombre_bodega, direccion, ciudad, tipo)
values (uuid(), 'Bodega 1', 'Calle 123 # 45 - 6', 'Bogotá', 'BODEGA');

insert into bodegas (id, nombre_bodega, direccion, ciudad, tipo)
values (uuid(), 'Bodega 2', 'Calle 321 # 45 - 6', 'Medellín', 'BODEGA');

insert into bodegas (id, nombre_bodega, direccion, ciudad, tipo)
values (uuid(), 'Centro de Distribución 1', 'Calle 132 # 45 - 6', 'Bogotá', 'CENTRO_DISTRIBUCION');

insert into inventario_bodega (bodega_id, item_id)
values ((select id from bodegas where nombre_bodega = 'Bodega 1'), 'item1');

insert into inventario_bodega (bodega_id, item_id)
values ((select id from bodegas where nombre_bodega = 'Bodega 2'), 'item1');

insert into inventario_bodega (bodega_id, item_id)
values ((select id from bodegas where nombre_bodega = 'Bodega 1'), 'item3');

insert into inventario_bodega (bodega_id, item_id)
values ((select id from bodegas where nombre_bodega = 'Bodega 2'), 'item2');

insert into inventario_bodega (bodega_id, item_id)
values ((select id from bodegas where nombre_bodega = 'Centro de Distribución 1'), 'item4');