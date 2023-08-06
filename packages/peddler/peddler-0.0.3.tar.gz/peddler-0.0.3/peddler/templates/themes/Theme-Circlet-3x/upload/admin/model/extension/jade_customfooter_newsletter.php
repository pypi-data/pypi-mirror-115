<?php
class ModelExtensionJadeCustomfooterNewsletter extends Model {
	public function editJadeNewsletter($newsletter_id, $data) {
		$this->db->query("UPDATE " . DB_PREFIX . "jade_customfooter_newsletter SET status = '" . (int)$data['status'] . "', language_id = '" . (int)$data['language_id'] . "', store_id = '" . (int)$data['store_id'] . "', date_modified = NOW() WHERE newsletter_id = '" . (int)$newsletter_id . "'");
	}

	public function deleteJadeNewsletter($newsletter_id) {
		$this->db->query("DELETE FROM " . DB_PREFIX . "jade_customfooter_newsletter WHERE newsletter_id = '" . (int)$newsletter_id . "'");
	}

	public function getJadeNewsletter($newsletter_id) {
		$query = $this->db->query("SELECT DISTINCT * FROM " . DB_PREFIX . "jade_customfooter_newsletter WHERE newsletter_id = '" . (int)$newsletter_id . "'");

		return $query->row;
	}

	public function getJadeNewsletters($data = array()) {
			$sql = "SELECT * FROM " . DB_PREFIX . "jade_customfooter_newsletter WHERE newsletter_id > '0'";

			if (!empty($data['filter_email'])) {
				$sql .= " AND email LIKE '" . $this->db->escape($data['filter_email']) . "%'";
			}

			if (isset($data['filter_status']) && !is_null($data['filter_status'])) {
				$sql .= " AND status = '" . (int)$data['filter_status'] . "'";
			}

			$sort_data = array(
				'email',
				'status',
				'ip',
				'date_added',
			);

			if (isset($data['sort']) && in_array($data['sort'], $sort_data)) {
				$sql .= " ORDER BY " . $data['sort'];
			} else {
				$sql .= " ORDER BY date_added";
			}

			if (isset($data['order']) && ($data['order'] == 'DESC')) {
				$sql .= " DESC";
			} else {
				$sql .= " ASC";
			}

			if (isset($data['start']) || isset($data['limit'])) {
				if ($data['start'] < 0) {
					$data['start'] = 0;
				}

				if ($data['limit'] < 1) {
					$data['limit'] = 20;
				}

				$sql .= " LIMIT " . (int)$data['start'] . "," . (int)$data['limit'];
			}

			$query = $this->db->query($sql);

			return $query->rows;
	}

	public function getTotalJadeNewsletters($data = array()) {
		$sql = "SELECT COUNT(*) AS total FROM " . DB_PREFIX . "jade_customfooter_newsletter WHERE newsletter_id > '0'";

		if (!empty($data['filter_email'])) {
			$sql .= " AND email LIKE '" . $this->db->escape($data['filter_email']) . "%'";
		}

		if (isset($data['filter_status']) && !is_null($data['filter_status'])) {
			$sql .= " AND status = '" . (int)$data['filter_status'] . "'";
		}

		$query = $this->db->query($sql);

		return $query->row['total'];
	}
}