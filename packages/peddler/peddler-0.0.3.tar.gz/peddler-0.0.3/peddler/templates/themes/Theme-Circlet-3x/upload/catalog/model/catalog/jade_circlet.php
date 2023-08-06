<?php
class ModelCatalogJadeCirclet extends Model {
	public function getProductAdditionalFirstImage($product_id) {
		$query = $this->db->query("SELECT * FROM " . DB_PREFIX . "product_image WHERE product_id = '" . (int)$product_id . "' ORDER BY sort_order ASC LIMIT 0, 1");

		return $query->row;
	}
}